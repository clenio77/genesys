"""
Microserviço 1: Document Uploader
Responsável por receber, validar e armazenar documentos
"""

import os
import hashlib
import aiofiles
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from src.config import Config
from src.models.document import Document


class DocumentUploader:
    """Gerenciador de upload e validação de documentos"""
    
    def __init__(self):
        self.upload_dir = Path(Config.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.max_size = Config.MAX_FILE_SIZE
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    def validate_file(self, file: UploadFile) -> bool:
        """
        Valida formato e tamanho do arquivo
        
        Args:
            file: Arquivo enviado
            
        Returns:
            True se válido, False caso contrário
        """
        # Verificar extensão
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            return False
        
        # Verificar tamanho (se disponível)
        if hasattr(file, 'size') and file.size > self.max_size:
            return False
        
        return True
    
    async def upload_file(self, file: UploadFile) -> Dict:
        """
        Faz upload do arquivo
        
        Args:
            file: Arquivo para upload
            
        Returns:
            Dict com informações do documento
        """
        if not self.validate_file(file):
            raise HTTPException(
                status_code=400,
                detail="Arquivo inválido"
            )
        
        # Gerar hash do arquivo
        content = await file.read()
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Criar nome único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(file.filename).suffix
        unique_filename = f"{timestamp}_{file_hash[:8]}{file_ext}"
        file_path = self.upload_dir / unique_filename
        
        # Salvar arquivo
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Virus scanning (se habilitado)
        if Config.ENABLE_VIRUS_SCAN:
            if not await self.scan_virus(file_path):
                file_path.unlink()  # Remove arquivo infectado
                raise HTTPException(
                    status_code=400,
                    detail="Arquivo infectado detectado"
                )
        
        # Criar registro do documento no banco
        # Nota: Este método agora precisa receber db: Session como parâmetro
        # Por enquanto retorna dict, será atualizado quando chamado com db
        document_data = {
            "filename": file.filename,
            "stored_filename": unique_filename,
            "file_path": str(file_path),
            "file_hash": file_hash,
            "file_size": len(content),
            "file_type": file_ext.replace('.', ''),
            "status": "uploaded"
        }
        
        return document_data
    
    async def scan_virus(self, file_path: Path) -> bool:
        """
        Escaneia arquivo em busca de vírus
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se seguro, False se infectado
        """
        # TODO: Implementar integração com ClamAV
        # Por enquanto retorna True (sem scan)
        return True
    
    async def get_document(self, document_id: int, db: Session) -> Optional[Document]:
        """
        Obtém documento por ID
        
        Args:
            document_id: ID do documento
            db: Sessão do banco de dados
            
        Returns:
            Document ou None
        """
        return db.query(Document).filter(Document.id == document_id).first()
    
    def create_document(self, document_data: Dict, db: Session) -> Document:
        """
        Cria documento no banco de dados
        
        Args:
            document_data: Dados do documento
            db: Sessão do banco de dados
            
        Returns:
            Document criado
        """
        # Verificar se já existe (pelo hash)
        existing = db.query(Document).filter(
            Document.file_hash == document_data["file_hash"]
        ).first()
        
        if existing:
            return existing
        
        # Criar novo documento
        document = Document(**document_data)
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
    
    async def list_documents(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None
    ) -> List[Document]:
        """
        Lista documentos
        
        Args:
            db: Sessão do banco de dados
            skip: Paginação - pular N registros
            limit: Limite de resultados
            status: Filtrar por status
            
        Returns:
            Lista de documentos
        """
        query = db.query(Document)
        
        if status:
            query = query.filter(Document.status == status)
        
        return query.order_by(desc(Document.uploaded_at)).offset(skip).limit(limit).all()
    
    async def get_stats(self, db: Session) -> Dict:
        """
        Obtém estatísticas dos documentos
        
        Args:
            db: Sessão do banco de dados
            
        Returns:
            Dict com estatísticas
        """
        total = db.query(Document).count()
        processed = db.query(Document).filter(Document.status == "processed").count()
        pending = db.query(Document).filter(Document.status.in_(["uploaded", "processing"])).count()
        failed = db.query(Document).filter(Document.status == "failed").count()
        
        # Calcular tamanho total
        total_size_result = db.query(func.sum(Document.file_size)).scalar()
        total_size = total_size_result if total_size_result else 0
        
        return {
            "total_documents": total,
            "processed": processed,
            "pending": pending,
            "failed": failed,
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }

