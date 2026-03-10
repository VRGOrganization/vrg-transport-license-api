"""Testes unitários para o serviço de preenchimento da carteirinha."""

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from app.schemas.student import Student
from app.services.fill_license import fill_license, _load_font, _export_image


class TestFillLicense:
    """Testes para a função fill_license."""
    
    def test_load_font_default(self):
        """Testa se a fonte padrão é carregada quando as TrueType não existem."""
        font = _load_font()
        assert font is not None
        
    def test_export_image(self, tmp_path: Path):
        """Testa a exportação de imagem para bytes."""
        # Cria uma imagem de teste
        img = Image.new('RGB', (100, 100), color='blue')
        
        # Exporta para bytes
        img_bytes = _export_image(img)
        
        # Verifica se é um bytes não vazio
        assert isinstance(img_bytes, bytes)
        assert len(img_bytes) > 0
        
        # Verifica se pode ser lido de volta como imagem
        result_img = Image.open(BytesIO(img_bytes))
        assert result_img.size == (100, 100)
        
    def test_fill_license_without_photo(self, valid_student_data):
        """Testa a geração da carteirinha sem foto."""
        student = Student(**valid_student_data)
        
        result = fill_license(student)
        
        assert isinstance(result, bytes)
        assert len(result) > 0
        
    def test_fill_license_with_photo(self, valid_student_data, sample_photo_base64):
        """Testa a geração da carteirinha com foto."""
        data = valid_student_data.copy()
        data["photo"] = sample_photo_base64
        student = Student(**data)
        
        result = fill_license(student)
        
        assert isinstance(result, bytes)
        assert len(result) > 0