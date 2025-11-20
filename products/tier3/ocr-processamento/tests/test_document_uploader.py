"""
Testes para Document Uploader
"""

import pytest
from fastapi import UploadFile
from io import BytesIO
from pathlib import Path

from src.services.document_uploader import DocumentUploader


class TestDocumentUploader:
    """Testes do Document Uploader"""
    
    def test_validate_file_valid_pdf(self):
        """Testa validação de PDF válido"""
        uploader = DocumentUploader()
        
        # Criar arquivo simulado
        file_content = b"PDF content"
        file = UploadFile(
            filename="test.pdf",
            file=BytesIO(file_content)
        )
        
        assert uploader.validate_file(file) == True
    
    def test_validate_file_invalid_extension(self):
        """Testa validação de extensão inválida"""
        uploader = DocumentUploader()
        
        file = UploadFile(
            filename="test.exe",
            file=BytesIO(b"content")
        )
        
        assert uploader.validate_file(file) == False
    
    def test_validate_file_allowed_extensions(self):
        """Testa extensões permitidas"""
        uploader = DocumentUploader()
        
        allowed = [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif"]
        
        for ext in allowed:
            file = UploadFile(
                filename=f"test{ext}",
                file=BytesIO(b"content")
            )
            assert uploader.validate_file(file) == True

