"""Testes de integração para a API de licenças."""

import base64
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.config import API_KEY


@pytest.mark.integration
class TestLicenseAPI:
    """Testes para o endpoint /license/create."""
    
    def test_create_license_success(self, client: TestClient, valid_student_data, api_key: str):
        """Testa criação bem-sucedida de carteirinha sem foto."""
        response = client.post(
            "/api/v1/license/create",
            json=valid_student_data,
            headers={"X-Api-Key": api_key}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "image" in data
        
        # Verifica se a imagem é válida
        image_bytes = base64.b64decode(data["image"])
        img = Image.open(BytesIO(image_bytes))
        assert img.size == (800, 600)  # Ajuste conforme seu template
        
    def test_create_license_with_photo(self, client: TestClient, valid_student_data, 
                                      sample_photo_base64, api_key: str):
        """Testa criação bem-sucedida de carteirinha com foto."""
        data = valid_student_data.copy()
        data["photo"] = sample_photo_base64
        
        response = client.post(
            "/api/v1/license/create",
            json=data,
            headers={"X-Api-Key": api_key}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "image" in data
        
    def test_create_license_unauthorized(self, client: TestClient, valid_student_data):
        """Testa acesso não autorizado (sem API key)."""
        response = client.post(
            "/api/v1/license/create",
            json=valid_student_data
        )
        
        assert response.status_code == 403
        assert "detalhe" in response.json().lower() or "detail" in response.json().lower()
        
    def test_create_license_wrong_key(self, client: TestClient, valid_student_data):
        """Testa acesso com chave API incorreta."""
        response = client.post(
            "/api/v1/license/create",
            json=valid_student_data,
            headers={"X-Api-Key": "wrong-key-123"}
        )
        
        assert response.status_code == 403
        
    def test_create_license_missing_fields(self, client: TestClient, api_key: str):
        """Testa envio com campos obrigatórios faltando."""
        incomplete_data = {
            "id": "12345",
            "name": "João da Silva"
            # Faltando degree, institution, etc
        }
        
        response = client.post(
            "/api/v1/license/create",
            json=incomplete_data,
            headers={"X-Api-Key": api_key}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
        
    @pytest.mark.parametrize("field", ["name", "degree", "institution"])
    def test_create_license_missing_specific_field(self, client: TestClient, 
                                                  valid_student_data, api_key: str, field: str):
        """Testa falta de campos específicos usando parametrização."""
        data = valid_student_data.copy()
        del data[field]
        
        response = client.post(
            "/api/v1/license/create",
            json=data,
            headers={"X-Api-Key": api_key}
        )
        
        assert response.status_code == 422