"""
Fixtures compartilhadas entre os testes.
"""
import base64
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client():
    """Cliente de teste para a API FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_api_key(monkeypatch):
    """Define uma API_KEY de teste."""
    test_key = "test-api-key-12345"
    monkeypatch.setattr("app.config.API_KEY", test_key)
    monkeypatch.setattr("app.routes.license.API_KEY", test_key)
    return test_key


@pytest.fixture
def mock_api_key_none(monkeypatch):
    """Define API_KEY como None (desabilita autenticação)."""
    monkeypatch.setattr("app.config.API_KEY", None)
    monkeypatch.setattr("app.routes.license.API_KEY", None)


@pytest.fixture
def valid_student_data():
    """Dados válidos de um estudante para testes."""
    return {
        "id": "2024001",
        "employee_id": "emp-0001",
        "name": "João da Silva",
        "degree": "Engenharia de Software",
        "institution": "UFPE",
        "shift": "Manhã",
        "telephone": "(81) 99999-9999",
        "blood_type": "O+",
        "bus": "123",
        "photo": base64.b64encode(b"fake_image_data").decode("utf-8")
    }


@pytest.fixture
def valid_student_data_no_photo(valid_student_data):
    """Dados válidos de um estudante sem foto."""
    data = valid_student_data.copy()
    data["photo"] = None
    return data


@pytest.fixture
def empty_student_data():
    """Dados de estudante com campos vazios (teste de validação)."""
    return {
        "id": "",
        "employee_id": "",
        "name": "",
        "degree": "",
        "institution": "",
        "shift": "",
        "telephone": "",
        "blood_type": "",
        "bus": "",
    }


@pytest.fixture
def mock_fill_license():
    """
    Mock da função fill_license para evitar I/O de imagem nos testes de rota.
    Retorna bytes simulados de uma imagem JPEG.
    """
    fake_image_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF"  # Header JPEG
    with patch("app.routes.license.fill_license", return_value=fake_image_bytes) as mock:
        yield mock
