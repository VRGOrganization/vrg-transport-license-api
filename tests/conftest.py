"""Fixtures compartilhadas para todos os testes."""

import base64
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.config import API_KEY


@pytest.fixture
def test_app() -> FastAPI:
    """Retorna a aplicação FastAPI para testes."""
    return app


@pytest.fixture
def client(test_app: FastAPI) -> Generator:
    """Retorna um cliente de teste para a aplicação."""
    with TestClient(test_app) as client:
        yield client


@pytest.fixture
def api_key() -> str:
    """Retorna a chave de API válida para testes."""
    return API_KEY or "test-key-123"


@pytest.fixture
def valid_student_data() -> Dict[str, Any]:
    """Retorna dados válidos de um estudante."""
    return {
        "id": "12345",
        "name": "João da Silva",
        "degree": "Engenharia de Software",
        "institution": "UFPE",
        "shift": "Manhã",
        "telephone": "(81) 99999-1234",
        "blood_type": "O+",
    }


@pytest.fixture
def sample_photo_base64() -> str:
    """Gera uma imagem de exemplo em base64 para testes."""
    # Cria uma imagem simples em memória
    img = Image.new('RGB', (200, 250), color='red')
    
    # Salva em bytes
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    
    # Retorna base64
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


@pytest.fixture
def assets_dir() -> Path:
    """Retorna o caminho para o diretório de assets."""
    return Path(__file__).parent.parent / "app" / "assets"


@pytest.fixture
def template_exists(assets_dir) -> bool:
    """Verifica se o template existe."""
    template_path = assets_dir / "modelo.jpg"
    return template_path.exists()