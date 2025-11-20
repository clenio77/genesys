"""
Microserviço 3: Data Extractor
Responsável por extrair dados estruturados do texto OCR
"""

import re
from typing import Dict, List, Optional
from datetime import datetime
from dateutil import parser as date_parser
from sqlalchemy.orm import Session

from src.config import Config
from src.models.document import Document, ExtractedData, OCRResult
from src.services.document_uploader import DocumentUploader


class DataExtractor:
    """Extrator de dados estruturados de documentos jurídicos"""
    
    def __init__(self):
        self.document_uploader = DocumentUploader()
        # Padrões regex para extração
        self.date_patterns = [
            r'\d{2}/\d{2}/\d{4}',
            r'\d{2}-\d{2}-\d{4}',
            r'\d{4}-\d{2}-\d{2}',
            r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}'
        ]
        
        self.money_patterns = [
            r'R\$\s*\d+[.,]\d{2}',
            r'\d+[.,]\d{2}\s*reais',
            r'valor\s*:\s*R\$\s*\d+[.,]\d{2}'
        ]
        
        self.cpf_pattern = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'
        self.cnpj_pattern = r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}'
        self.process_number_pattern = r'\d{7}-?\d{2}\.?\d{4}\.?\d{1}\.?\d{2}\.?\d{4}'
    
    async def extract(self, document_id: int, db: Session) -> List[ExtractedData]:
        """
        Extrai dados estruturados do documento e salva no banco
        
        Args:
            document_id: ID do documento
            db: Sessão do banco de dados
            
        Returns:
            Lista de ExtractedData salvos no banco
        """
        # Buscar texto OCR do banco
        ocr_result = db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        if not ocr_result:
            raise ValueError(f"OCR não encontrado para documento {document_id}")
        
        # Remover dados extraídos anteriores
        db.query(ExtractedData).filter(
            ExtractedData.document_id == document_id
        ).delete()
        
        # Extrair dados do texto
        extracted_dict = await self.extract_from_text(ocr_result.text)
        
        # Salvar no banco
        extracted_items = []
        
        # Salvar prazos
        for prazo in extracted_dict.get("prazos", []):
            item = ExtractedData(
                document_id=document_id,
                field="prazo",
                value=prazo.get("text", ""),
                confidence=0.85,
                metadata={"value": prazo.get("value"), "position": prazo.get("position")}
            )
            db.add(item)
            extracted_items.append(item)
        
        # Salvar valores
        for valor in extracted_dict.get("valores", []):
            item = ExtractedData(
                document_id=document_id,
                field="valor",
                value=str(valor.get("value", "")),
                confidence=valor.get("confidence", 0.85),
                metadata={"currency": valor.get("currency"), "position": valor.get("position")}
            )
            db.add(item)
            extracted_items.append(item)
        
        # Salvar partes
        for parte in extracted_dict.get("partes", []):
            item = ExtractedData(
                document_id=document_id,
                field="parte",
                value=parte.get("name", ""),
                confidence=0.85,
                metadata={"role": parte.get("role"), "position": parte.get("position")}
            )
            db.add(item)
            extracted_items.append(item)
        
        # Salvar processo
        if extracted_dict.get("processo"):
            item = ExtractedData(
                document_id=document_id,
                field="processo",
                value=extracted_dict["processo"],
                confidence=0.90
            )
            db.add(item)
            extracted_items.append(item)
        
        # Salvar CPFs
        for cpf in extracted_dict.get("cpfs", []):
            item = ExtractedData(
                document_id=document_id,
                field="cpf",
                value=cpf,
                confidence=0.95
            )
            db.add(item)
            extracted_items.append(item)
        
        # Salvar CNPJs
        for cnpj in extracted_dict.get("cnpjs", []):
            item = ExtractedData(
                document_id=document_id,
                field="cnpj",
                value=cnpj,
                confidence=0.95
            )
            db.add(item)
            extracted_items.append(item)
        
        # Salvar datas
        for data in extracted_dict.get("datas", []):
            item = ExtractedData(
                document_id=document_id,
                field="data",
                value=data.get("parsed", data.get("text", "")),
                confidence=0.90,
                metadata={"text": data.get("text"), "position": data.get("position")}
            )
            db.add(item)
            extracted_items.append(item)
        
        db.commit()
        
        # Refresh all items
        for item in extracted_items:
            db.refresh(item)
        
        return extracted_items
    
    async def extract_from_text(self, text: str) -> Dict:
        """
        Extrai dados de um texto
        
        Args:
            text: Texto para extrair dados
            
        Returns:
            Dict com dados extraídos
        """
        extracted = {
            "prazos": self.extract_prazos(text),
            "valores": self.extract_valores(text),
            "partes": self.extract_partes(text),
            "processo": self.extract_processo(text),
            "cpfs": self.extract_cpfs(text),
            "cnpjs": self.extract_cnpjs(text),
            "datas": self.extract_datas(text),
            "confidence": 0.85
        }
        
        return extracted
    
    def extract_prazos(self, text: str) -> List[Dict]:
        """
        Extrai prazos do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de prazos encontrados
        """
        prazos = []
        
        # Padrões de prazo
        prazo_patterns = [
            r'prazo\s+de\s+(\d+)\s+dias',
            r'(\d+)\s+dias\s+para',
            r'vencimento\s+em\s+(\d{2}/\d{2}/\d{4})',
            r'prazo\s+até\s+(\d{2}/\d{2}/\d{4})'
        ]
        
        for pattern in prazo_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                prazos.append({
                    "text": match.group(0),
                    "value": match.group(1) if match.groups() else None,
                    "position": match.start()
                })
        
        return prazos
    
    def extract_valores(self, text: str) -> List[Dict]:
        """
        Extrai valores monetários do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de valores encontrados
        """
        valores = []
        
        for pattern in self.money_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                value_text = match.group(0)
                # Extrair número
                number_match = re.search(r'\d+[.,]\d{2}', value_text)
                if number_match:
                    value = float(number_match.group(0).replace(',', '.'))
                    valores.append({
                        "text": value_text,
                        "value": value,
                        "currency": "BRL",
                        "position": match.start()
                    })
        
        return valores
    
    def extract_partes(self, text: str) -> List[Dict]:
        """
        Extrai partes envolvidas (autor, réu, etc)
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de partes encontradas
        """
        partes = []
        
        # Padrões de partes
        parte_patterns = [
            r'autor[ae]?s?[:\s]+([A-Z][A-Za-z\s]+)',
            r'réu[us]?[:\s]+([A-Z][A-Za-z\s]+)',
            r'requerente[:\s]+([A-Z][A-Za-z\s]+)',
            r'requerido[:\s]+([A-Z][A-Za-z\s]+)'
        ]
        
        for pattern in parte_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                partes.append({
                    "role": self._identify_role(match.group(0)),
                    "name": match.group(1).strip(),
                    "position": match.start()
                })
        
        return partes
    
    def extract_processo(self, text: str) -> Optional[str]:
        """
        Extrai número do processo
        
        Args:
            text: Texto para análise
            
        Returns:
            Número do processo ou None
        """
        matches = re.finditer(self.process_number_pattern, text)
        for match in matches:
            return match.group(0)
        return None
    
    def extract_cpfs(self, text: str) -> List[str]:
        """
        Extrai CPFs do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de CPFs encontrados
        """
        matches = re.findall(self.cpf_pattern, text)
        return list(set(matches))  # Remove duplicatas
    
    def extract_cnpjs(self, text: str) -> List[str]:
        """
        Extrai CNPJs do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de CNPJs encontrados
        """
        matches = re.findall(self.cnpj_pattern, text)
        return list(set(matches))  # Remove duplicatas
    
    def extract_datas(self, text: str) -> List[Dict]:
        """
        Extrai datas do texto
        
        Args:
            text: Texto para análise
            
        Returns:
            Lista de datas encontradas
        """
        datas = []
        
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                date_str = match.group(0)
                try:
                    # Tentar parsear data
                    parsed_date = date_parser.parse(date_str, dayfirst=True)
                    datas.append({
                        "text": date_str,
                        "parsed": parsed_date.isoformat(),
                        "position": match.start()
                    })
                except:
                    pass
        
        return datas
    
    def _identify_role(self, text: str) -> str:
        """Identifica o papel da parte"""
        text_lower = text.lower()
        if 'autor' in text_lower:
            return 'autor'
        elif 'réu' in text_lower:
            return 'réu'
        elif 'requerente' in text_lower:
            return 'requerente'
        elif 'requerido' in text_lower:
            return 'requerido'
        return 'outro'

