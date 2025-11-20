"""
Microserviço 5: Classifier
Responsável por classificação automática de documentos
"""

from typing import Dict, List, Optional
from datetime import datetime
import re
from sqlalchemy.orm import Session

from src.config import Config
from src.models.document import Document, DocumentClassification, OCRResult
from src.services.document_uploader import DocumentUploader


class Classifier:
    """Classificador automático de documentos jurídicos"""
    
    def __init__(self):
        self.document_uploader = DocumentUploader()
        # Categorias de documentos jurídicos
        self.categories = {
            "petição_inicial": {
                "keywords": ["petição inicial", "requer", "requerente", "venho por meio desta"],
                "keywords_negative": []
            },
            "contestações": {
                "keywords": ["contesta", "réu", "contestar", "defesa"],
                "keywords_negative": []
            },
            "sentenças": {
                "keywords": ["sentença", "julgamento", "procedo", "não procedo", "julgo"],
                "keywords_negative": []
            },
            "despachos": {
                "keywords": ["despacho", "determino", "determina"],
                "keywords_negative": []
            },
            "intimações": {
                "keywords": ["intimação", "intimado", "prazo", "para manifestar"],
                "keywords_negative": []
            },
            "certidões": {
                "keywords": ["certidão", "certifico", "informo que"],
                "keywords_negative": []
            },
            "mandados": {
                "keywords": ["mandado", "cumprir", "determina-se"],
                "keywords_negative": []
            },
            "alvarás": {
                "keywords": ["alvará", "autorizo", "permissão"],
                "keywords_negative": []
            },
            "contratos": {
                "keywords": ["contrato", "contratante", "contratado", "cláusula"],
                "keywords_negative": []
            },
            "outros": {
                "keywords": [],
                "keywords_negative": []
            }
        }
        
        # Níveis de urgência
        self.urgency_keywords = {
            "urgente": ["urgente", "imediatamente", "hoje", "prazo vencido", "vencido"],
            "alta": ["prazo", "até", "máximo", "importante"],
            "média": ["manifestar", "responder", "prazo de"],
            "baixa": ["informação", "consulta", "solicitação"]
        }
    
    async def classify(self, document_id: int, db: Session) -> DocumentClassification:
        """
        Classifica documento e salva no banco
        
        Args:
            document_id: ID do documento
            db: Sessão do banco de dados
            
        Returns:
            DocumentClassification salvo no banco
        """
        # Verificar se já existe classificação
        existing_classification = db.query(DocumentClassification).filter(
            DocumentClassification.document_id == document_id
        ).first()
        
        if existing_classification:
            return existing_classification
        
        # Buscar texto OCR do banco
        ocr_result = db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        if not ocr_result:
            raise ValueError(f"OCR não encontrado para documento {document_id}")
        
        # Classificar texto
        classification_dict = await self.classify_text(ocr_result.text)
        
        # Salvar no banco
        classification = DocumentClassification(
            document_id=document_id,
            category=classification_dict["category"],
            confidence=classification_dict["category_confidence"],
            urgency=classification_dict["urgency"],
            urgency_confidence=classification_dict["urgency_confidence"],
            tags=classification_dict["tags"]
        )
        
        db.add(classification)
        db.commit()
        db.refresh(classification)
        
        return classification
    
    async def classify_text(self, text: str) -> Dict:
        """
        Classifica texto diretamente
        
        Args:
            text: Texto para classificar
            
        Returns:
            Dict com classificação
        """
        text_lower = text.lower()
        
        # Classificar categoria
        category_scores = {}
        for category, patterns in self.categories.items():
            score = 0
            keywords = patterns.get("keywords", [])
            keywords_negative = patterns.get("keywords_negative", [])
            
            # Pontos positivos
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            # Pontos negativos
            for keyword in keywords_negative:
                if keyword in text_lower:
                    score -= 1
            
            if score > 0:
                category_scores[category] = score
        
        # Determinar categoria
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            confidence = min(category_scores[best_category] / 5.0, 1.0)
        else:
            best_category = "outros"
            confidence = 0.5
        
        # Classificar urgência
        urgency_scores = {}
        for urgency_level, keywords in self.urgency_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                urgency_scores[urgency_level] = score
        
        if urgency_scores:
            best_urgency = max(urgency_scores, key=urgency_scores.get)
            urgency_confidence = min(urgency_scores[best_urgency] / 3.0, 1.0)
        else:
            best_urgency = "média"
            urgency_confidence = 0.5
        
        # Extrair tags
        tags = self._extract_tags(text_lower, best_category)
        
        return {
            "category": best_category,
            "category_confidence": confidence,
            "urgency": best_urgency,
            "urgency_confidence": urgency_confidence,
            "tags": tags
        }
    
    def _extract_tags(self, text: str, category: str) -> List[str]:
        """
        Extrai tags relevantes do texto
        
        Args:
            text: Texto em minúsculas
            category: Categoria do documento
            
        Returns:
            Lista de tags
        """
        tags = []
        
        # Tags baseadas em conteúdo
        if "honorários" in text or "honorario" in text:
            tags.append("honorários")
        
        if "danos" in text or "indenização" in text:
            tags.append("indenização")
        
        if "tutela" in text or "tutela antecipada" in text:
            tags.append("tutela_antecipada")
        
        if "liminar" in text:
            tags.append("liminar")
        
        if "recurso" in text:
            tags.append("recurso")
        
        if "apelação" in text:
            tags.append("apelação")
        
        if "embargos" in text:
            tags.append("embargos")
        
        # Tags baseadas em valores
        if re.search(r'r\$\s*\d+', text):
            tags.append("com_valor")
        
        # Tags baseadas em prazos
        if re.search(r'\d+\s+dias', text):
            tags.append("com_prazo")
        
        return tags

