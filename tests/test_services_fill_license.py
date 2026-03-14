"""
Testes para o serviço fill_license
"""
from io import BytesIO
from unittest.mock import MagicMock, Mock, patch

import pytest
from PIL import Image

from app.errors import AppError
from app.schemas.student import Student
from app.services.fill_license import (
    _export_image,
    _load_font,
    _paste_photo,
    _write_fields,
    fill_license,
)


class TestLoadFont:
    """Testes da função _load_font"""
    
    @patch("app.services.fill_license.ImageFont")
    def test_load_font_success(self, mock_image_font):
        """Teste de carregamento de fonte com sucesso."""
        mock_font = Mock()
        mock_image_font.truetype.return_value = mock_font
        
        result = _load_font(20)
        
        assert result == mock_font
        mock_image_font.truetype.assert_called()
    
    @patch("app.services.fill_license.ImageFont")
    def test_load_font_fallback_to_default(self, mock_image_font):
        """Teste de fallback para fonte padrão quando arquivo não existe."""
        mock_image_font.truetype.side_effect = OSError("Font not found")
        mock_default = Mock()
        mock_image_font.load_default.return_value = mock_default
        
        result = _load_font(20)
        
        assert result == mock_default
        mock_image_font.load_default.assert_called_once()


class TestWriteFields:
    """Testes da função _write_fields"""
    
    @patch("app.services.fill_license._load_font")
    def test_write_fields_calls_draw_text(self, mock_load_font, valid_student_data):
        """Teste que todos os campos são escritos na imagem."""
        mock_font = Mock()
        mock_load_font.return_value = mock_font
        
        mock_draw = Mock()
        student = Student(**valid_student_data)
        
        _write_fields(mock_draw, student)
        
        # Verifica que draw.text foi chamado para cada campo
        assert mock_draw.text.call_count >= 7  # 7 campos (name, institution, degree, etc)
        
        # Verifica que pelo menos o nome foi escrito
        calls = [str(call) for call in mock_draw.text.call_args_list]
        assert any(valid_student_data["name"] in str(call) for call in calls)


class TestPastePhoto:
    """Testes da função _paste_photo"""
    
    @patch("app.services.fill_license.Image")
    def test_paste_photo_success(self, mock_image_class):
        """Teste de colagem de foto com sucesso."""
        import base64
        
        # Mock do template
        mock_template = Mock()
        
        # Mock da foto carregada
        mock_photo = Mock()
        mock_photo.resize.return_value = mock_photo
        mock_image_class.open.return_value = mock_photo
        
        photo_base64 = base64.b64encode(b"fake_photo_data").decode()
        
        _paste_photo(mock_template, photo_base64)
        
        # Verifica que a foto foi aberta, convertida, redimensionada e colada
        mock_image_class.open.assert_called_once()
        mock_photo.convert.assert_called_once_with("RGB")
        mock_template.paste.assert_called_once()
    
    @patch("app.services.fill_license.Image")
    def test_paste_photo_with_invalid_base64(self, mock_image_class):
        """Teste com base64 inválido - deve levantar exceção."""
        mock_template = Mock()
        
        with pytest.raises(AppError) as exc_info:
            _paste_photo(mock_template, "invalid_base64!@#")

        assert exc_info.value.code == "ERR002"
        assert exc_info.value.status == 400


class TestExportImage:
    """Testes da função _export_image"""
    
    def test_export_image_returns_bytes(self):
        """Teste que _export_image retorna bytes."""
        # Cria uma imagem real pequena para testar
        mock_image = Image.new("RGB", (100, 100), color="white")
        
        result = _export_image(mock_image)
        
        assert isinstance(result, bytes)
        assert len(result) > 0
        # Verifica que começa com header JPEG
        assert result[:2] == b"\xff\xd8"  # JPEG magic bytes


class TestFillLicense:
    """Testes da função principal fill_license"""
    
    @patch("app.services.fill_license.Image")
    @patch("app.services.fill_license._write_fields")
    @patch("app.services.fill_license._export_image")
    def test_fill_license_without_photo(
        self, mock_export, mock_write, mock_image_class, valid_student_data_no_photo
    ):
        """Teste de geração de carteirinha sem foto."""
        # Setup mocks
        mock_template = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_template
        mock_export.return_value = b"fake_jpeg_bytes"
        
        student = Student(**valid_student_data_no_photo)
        result = fill_license(student)
        
        # Verificações
        mock_image_class.open.assert_called_once()
        mock_write.assert_called_once()
        mock_export.assert_called_once()
        assert result == b"fake_jpeg_bytes"
    
    @patch("app.services.fill_license.Image")
    @patch("app.services.fill_license._paste_photo")
    @patch("app.services.fill_license._write_fields")
    @patch("app.services.fill_license._export_image")
    def test_fill_license_with_photo(
        self, mock_export, mock_write, mock_paste, mock_image_class, valid_student_data
    ):
        """Teste de geração de carteirinha com foto."""
        # Setup mocks
        mock_template = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_template
        mock_export.return_value = b"fake_jpeg_bytes"
        
        student = Student(**valid_student_data)
        result = fill_license(student)
        
        # Verificações
        mock_image_class.open.assert_called_once()
        mock_paste.assert_called_once_with(mock_template, valid_student_data["photo"])
        mock_write.assert_called_once()
        mock_export.assert_called_once()
        assert result == b"fake_jpeg_bytes"
    
    @patch("app.services.fill_license.Image")
    def test_fill_license_template_not_found(self, mock_image_class, valid_student_data):
        """Teste quando template não é encontrado."""
        mock_image_class.open.side_effect = FileNotFoundError("Template not found")
        
        student = Student(**valid_student_data)
        
        with pytest.raises(AppError) as exc_info:
            fill_license(student)
        
        assert exc_info.value.code == "ERR010"
        assert exc_info.value.status == 500
