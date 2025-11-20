"""
Microserviço 4: AI Analyzer
Responsável por análise inteligente com GPT-4
"""

from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from src.config import Config
from src.models.document import Document, AnalysisResult, OCRResult
from src.services.document_uploader import DocumentUploader


class AIAnalyzer:
    """Analisador de documentos usando GPT-4"""
    
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.AI_ANALYSIS_MODEL
        self.max_tokens = Config.MAX_TOKENS_ANALYSIS
        self.document_uploader = DocumentUploader()
        
        if self.api_key and OPENAI_AVAILABLE:
            self.openai_client = OpenAI(api_key=self.api_key)
        else:
            self.openai_client = None
    
    async def analyze(self, document_id: int, db: Session) -> AnalysisResult:
        """
        Analisa documento completo com IA e salva no banco
        
        Args:
            document_id: ID do documento
            db: Sessão do banco de dados
            
        Returns:
            AnalysisResult salvo no banco
        """
        # Verificar se já existe análise
        existing_analysis = db.query(AnalysisResult).filter(
            AnalysisResult.document_id == document_id
        ).first()
        
        if existing_analysis:
            return existing_analysis
        
        # Buscar texto OCR do banco
        ocr_result = db.query(OCRResult).filter(
            OCRResult.document_id == document_id
        ).first()
        
        if not ocr_result:
            raise ValueError(f"OCR não encontrado para documento {document_id}")
        
        # Analisar texto com IA
        analysis_dict = await self.analyze_text(ocr_result.text)
        
        # Salvar no banco
        analysis = AnalysisResult(
            document_id=document_id,
            summary=analysis_dict.get("summary", ""),
            key_points=analysis_dict.get("key_points", []),
            risk_score=analysis_dict.get("risk_score", 5.0),
            recommendations=analysis_dict.get("recommendations", []),
            sentiment=analysis_dict.get("sentiment", "neutral"),
            confidence=analysis_dict.get("confidence", 0.0)
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return analysis
    
    async def analyze_text(self, text: str) -> Dict:
        """
        Analisa texto com GPT-4
        
        Args:
            text: Texto para análise
            
        Returns:
            Dict com análise
        """
        if not self.openai_client:
            return self._default_analysis()
        
        try:
            prompt = self._build_analysis_prompt(text)
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente jurídico especializado em análise de documentos processuais."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parsear resposta estruturada
            return self._parse_analysis(analysis_text)
        
        except Exception as e:
            print(f"Erro na análise IA: {e}")
            return self._default_analysis()
    
    def _build_analysis_prompt(self, text: str) -> str:
        """
        Constrói prompt para análise
        
        Args:
            text: Texto do documento
            
        Returns:
            Prompt formatado
        """
        # Limitar tamanho do texto (GPT-4 tem limite de tokens)
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        prompt = f"""
Analise o seguinte documento jurídico e forneça:

1. RESUMO: Um resumo conciso do documento (2-3 parágrafos)
2. PONTOS-CHAVE: Lista com 5-7 pontos principais
3. ANÁLISE DE RISCO: Score de 0-10 indicando risco processual
4. RECOMENDAÇÕES: 3-5 recomendações de ação
5. SENTIMENTO: positivo, neutro ou negativo

DOCUMENTO:
{text}

Responda em formato JSON estruturado.
"""
        return prompt
    
    def _parse_analysis(self, analysis_text: str) -> Dict:
        """
        Parseia resposta da IA
        
        Args:
            analysis_text: Texto da resposta
            
        Returns:
            Dict estruturado
        """
        # Tentar extrair JSON da resposta
        import json
        import re
        
        # Procurar JSON na resposta
        json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(0))
                return {
                    "summary": parsed.get("resumo", ""),
                    "key_points": parsed.get("pontos_chave", []),
                    "risk_score": float(parsed.get("risco", 5.0)),
                    "recommendations": parsed.get("recomendacoes", []),
                    "sentiment": parsed.get("sentimento", "neutral"),
                    "confidence": 0.9
                }
            except:
                pass
        
        # Fallback: extrair informações manualmente
        return {
            "summary": self._extract_summary(analysis_text),
            "key_points": self._extract_key_points(analysis_text),
            "risk_score": self._extract_risk_score(analysis_text),
            "recommendations": self._extract_recommendations(analysis_text),
            "sentiment": self._extract_sentiment(analysis_text),
            "confidence": 0.7
        }
    
    def _extract_summary(self, text: str) -> str:
        """Extrai resumo do texto"""
        lines = text.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            if 'resumo' in line.lower() or 'summary' in line.lower():
                in_summary = True
                continue
            if in_summary and line.strip():
                if any(keyword in line.lower() for keyword in ['pontos', 'análise', 'recomendações']):
                    break
                summary_lines.append(line.strip())
        
        return ' '.join(summary_lines[:3]) if summary_lines else text[:200]
    
    def _extract_key_points(self, text: str) -> list:
        """Extrai pontos-chave"""
        points = []
        lines = text.split('\n')
        in_points = False
        
        for line in lines:
            if 'pontos' in line.lower() or 'key points' in line.lower():
                in_points = True
                continue
            if in_points:
                if line.strip().startswith(('-', '*', '•', '1.', '2.')):
                    points.append(line.strip())
                if len(points) >= 7:
                    break
        
        return points[:7] if points else []
    
    def _extract_risk_score(self, text: str) -> float:
        """Extrai score de risco"""
        import re
        risk_match = re.search(r'risco[:\s]+(\d+\.?\d*)', text, re.IGNORECASE)
        if risk_match:
            return float(risk_match.group(1))
        return 5.0
    
    def _extract_recommendations(self, text: str) -> list:
        """Extrai recomendações"""
        recommendations = []
        lines = text.split('\n')
        in_recommendations = False
        
        for line in lines:
            if 'recomenda' in line.lower():
                in_recommendations = True
                continue
            if in_recommendations:
                if line.strip().startswith(('-', '*', '•', '1.', '2.')):
                    recommendations.append(line.strip())
                if len(recommendations) >= 5:
                    break
        
        return recommendations[:5] if recommendations else []
    
    def _extract_sentiment(self, text: str) -> str:
        """Extrai sentimento"""
        text_lower = text.lower()
        if any(word in text_lower for word in ['positivo', 'favorável', 'bom']):
            return 'positive'
        elif any(word in text_lower for word in ['negativo', 'desfavorável', 'ruim']):
            return 'negative'
        return 'neutral'
    
    def _default_analysis(self) -> Dict:
        """Retorna análise padrão quando IA não disponível"""
        return {
            "summary": "Análise não disponível - API não configurada",
            "key_points": [],
            "risk_score": 5.0,
            "recommendations": [],
            "sentiment": "neutral",
            "confidence": 0.0
        }

