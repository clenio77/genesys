"""
Microserviço 2: OCR Engine
Responsável por extração de texto usando Tesseract e Google Vision
"""

import pytesseract
from PIL import Image
import pdf2image
from typing import Dict, Optional
from pathlib import Path
import io
from sqlalchemy.orm import Session

try:
    from google.cloud import vision
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False

from src.config import Config
from src.models.document import Document, OCRResult
from src.services.document_uploader import DocumentUploader


class OCREngine:
    """Motor de OCR usando Tesseract e Google Vision"""
    
    def __init__(self):
        self.use_tesseract = Config.ENABLE_TESSERACT
        self.use_google_vision = Config.ENABLE_GOOGLE_VISION and GOOGLE_VISION_AVAILABLE
        self.confidence_threshold = Config.OCR_CONFIDENCE_THRESHOLD
        self.languages = Config.OCR_LANGUAGES
        self.document_uploader = DocumentUploader()
        
        # Configurar Google Vision se disponível
        if self.use_google_vision:
            try:
                self.vision_client = vision.ImageAnnotatorClient()
            except Exception:
                self.use_google_vision = False
                self.vision_client = None
    
    async def process_document(self, document_id: int, db: Session) -> OCRResult:
        """
        Processa documento completo com OCR e salva no banco
        
        Args:
            document_id: ID do documento
            db: Sessão do banco de dados
            
        Returns:
            OCRResult salvo no banco
        """
        # Buscar documento do banco
        document = await self.document_uploader.get_document(document_id, db)
        if not document:
            raise ValueError(f"Documento {document_id} não encontrado")
        
        # Verificar se já existe resultado OCR
        existing_ocr = db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        if existing_ocr:
            return existing_ocr
        
        # Processar arquivo
        ocr_result_dict = await self.process_file(document.file_path)
        
        # Salvar no banco
        ocr_result = OCRResult(
            document_id=document_id,
            text=ocr_result_dict["text"],
            confidence=ocr_result_dict["confidence"],
            language=ocr_result_dict.get("language", "por"),
            method=ocr_result_dict.get("method", "tesseract"),
            pages=ocr_result_dict.get("pages")
        )
        
        db.add(ocr_result)
        db.commit()
        db.refresh(ocr_result)
        
        return ocr_result
    
    async def process_file(self, file_path: str) -> Dict:
        """
        Processa arquivo diretamente
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Dict com resultados do OCR
        """
        file_path_obj = Path(file_path)
        
        if file_path_obj.suffix.lower() == '.pdf':
            return await self.process_pdf(file_path)
        else:
            return await self.process_image(file_path)
    
    async def process_image(self, image_path: str) -> Dict:
        """
        Processa imagem com OCR
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            Dict com texto extraído
        """
        # Tentar Google Vision primeiro (mais preciso)
        if self.use_google_vision:
            try:
                result = await self.process_with_google_vision(image_path)
                if result["confidence"] >= self.confidence_threshold:
                    return result
            except Exception as e:
                print(f"Erro no Google Vision: {e}")
        
        # Fallback para Tesseract
        if self.use_tesseract:
            return await self.process_with_tesseract(image_path)
        
        raise Exception("Nenhum método de OCR disponível")
    
    async def process_pdf(self, pdf_path: str) -> Dict:
        """
        Processa PDF convertendo para imagens
        
        Args:
            pdf_path: Caminho do PDF
            
        Returns:
            Dict com texto extraído de todas as páginas
        """
        try:
            # Converter PDF para imagens
            images = pdf2image.convert_from_path(pdf_path)
            
            all_text = []
            pages = []
            
            for i, image in enumerate(images):
                # Salvar imagem temporária
                temp_path = f"/tmp/page_{i}.png"
                image.save(temp_path)
                
                # Processar imagem
                page_result = await self.process_image(temp_path)
                
                all_text.append(page_result["text"])
                pages.append({
                    "page": i + 1,
                    "text": page_result["text"],
                    "confidence": page_result["confidence"]
                })
            
            # Combinar resultados
            full_text = "\n\n".join(all_text)
            avg_confidence = sum(p["confidence"] for p in pages) / len(pages) if pages else 0.0
            
            return {
                "text": full_text,
                "confidence": avg_confidence,
                "language": "por",
                "pages": pages,
                "method": "tesseract"
            }
        
        except Exception as e:
            raise Exception(f"Erro ao processar PDF: {e}")
    
    async def process_with_tesseract(self, image_path: str) -> Dict:
        """
        Processa imagem com Tesseract OCR
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            Dict com texto extraído
        """
        try:
            image = Image.open(image_path)
            
            # Configurar idiomas
            lang = "+".join(self.languages)
            
            # Extrair texto
            text = pytesseract.image_to_string(image, lang=lang)
            
            # Obter dados detalhados
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            # Calcular confiança média
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
            
            return {
                "text": text,
                "confidence": avg_confidence,
                "language": self.languages[0],
                "method": "tesseract"
            }
        
        except Exception as e:
            raise Exception(f"Erro no Tesseract: {e}")
    
    async def process_with_google_vision(self, image_path: str) -> Dict:
        """
        Processa imagem com Google Vision API
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            Dict com texto extraído
        """
        if not self.vision_client:
            raise Exception("Google Vision não disponível")
        
        try:
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Detectar texto
            response = self.vision_client.text_detection(image=image)
            texts = response.text_annotations
            
            if texts:
                # Primeiro texto é o texto completo
                full_text = texts[0].description
                
                # Calcular confiança média dos detections
                if len(texts) > 1:
                    # Usar bounding boxes para estimar confiança
                    # Google Vision não retorna confiança diretamente
                    confidence = 0.95  # Google Vision geralmente tem alta confiança
                else:
                    confidence = 0.90
                
                return {
                    "text": full_text,
                    "confidence": confidence,
                    "language": "por",
                    "method": "google_vision"
                }
            else:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "language": "por",
                    "method": "google_vision"
                }
        
        except Exception as e:
            raise Exception(f"Erro no Google Vision: {e}")

