"""
Testes para a rota /license/create
"""
import base64

import pytest


class TestLicenseCreate:
    """Testes da rota POST /license/create"""
    
    def test_create_license_success(
        self, test_client, mock_api_key, valid_student_data, mock_fill_license
    ):
        """Teste com dados válidos e API key correta - deve retornar 201 com imagem."""
        response = test_client.post(
            "/api/v1/license/create",
            json=valid_student_data,
            headers={"X-Api-Key": mock_api_key}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "image" in data
        assert isinstance(data["image"], str)
        
        # Verifica se é base64 válido
        try:
            base64.b64decode(data["image"])
        except Exception:
            pytest.fail("Imagem retornada não é base64 válido")
        
        # Verifica se fill_license foi chamado
        mock_fill_license.assert_called_once()
    
    def test_create_license_without_photo(
        self, test_client, mock_api_key, valid_student_data_no_photo, mock_fill_license
    ):
        """Teste com dados válidos mas sem foto - deve funcionar."""
        response = test_client.post(
            "/api/v1/license/create",
            json=valid_student_data_no_photo,
            headers={"X-Api-Key": mock_api_key}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "image" in data
    
    def test_create_license_invalid_api_key(
        self, test_client, mock_api_key, valid_student_data
    ):
        """Teste com API key inválida - deve retornar 403."""
        response = test_client.post(
            "/api/v1/license/create",
            json=valid_student_data,
            headers={"X-Api-Key": "wrong-key"}
        )
        
        assert response.status_code == 403
        assert response.json() == {"code": "ERR001", "status": 403}
    
    def test_create_license_missing_api_key(
        self, test_client, mock_api_key, valid_student_data
    ):
        """Teste sem API key no header - deve retornar 403."""
        response = test_client.post(
            "/api/v1/license/create",
            json=valid_student_data
        )
        
        assert response.status_code == 403
        assert response.json() == {"code": "ERR001", "status": 403}
    
    def test_create_license_no_auth_configured(
        self, test_client, mock_api_key_none, valid_student_data, mock_fill_license
    ):
        """Teste quando API_KEY não está configurada - deve permitir acesso."""
        response = test_client.post(
            "/api/v1/license/create",
            json=valid_student_data
        )
        
        assert response.status_code == 201
    
    def test_create_license_missing_required_field(
        self, test_client, mock_api_key, valid_student_data
    ):
        """Teste com campo obrigatório faltando - deve retornar 422."""
        incomplete_data = valid_student_data.copy()
        del incomplete_data["name"]  # Remove campo obrigatório
        
        response = test_client.post(
            "/api/v1/license/create",
            json=incomplete_data,
            headers={"X-Api-Key": mock_api_key}
        )
        
        assert response.status_code == 422
        # FastAPI/Pydantic retorna erro de validação
        assert "detail" in response.json()
    
    def test_create_license_empty_fields(
        self, test_client, mock_api_key, empty_student_data
    ):
        """
        Teste com campos vazios - deve retornar 422.
        Após adicionar Field(min_length=1), strings vazias são rejeitadas.
        """
        response = test_client.post(
            "/api/v1/license/create",
            json=empty_student_data,
            headers={"X-Api-Key": mock_api_key}
        )
        
        # FastAPI/Pydantic retorna 422 para campos vazios
        assert response.status_code == 422
        assert "detail" in response.json()
    
    def test_create_license_invalid_data_type(
        self, test_client, mock_api_key
    ):
        """Teste com tipo de dado inválido - deve retornar 422."""
        invalid_data = {
            "id": 123,  # Deveria ser string
            "name": "João",
            "degree": "Engenharia",
            "institution": "UFPE",
            "shift": "Manhã",
            "telephone": "(81) 99999-9999",
            "blood_type": "O+",
            "bus": "123"
        }
        
        response = test_client.post(
            "/api/v1/license/create",
            json=invalid_data,
            headers={"X-Api-Key": mock_api_key}
        )
        
        assert response.status_code == 422
    
    def test_create_license_empty_body(
        self, test_client, mock_api_key
    ):
        """Teste com body vazio - deve retornar 422."""
        response = test_client.post(
            "/api/v1/license/create",
            json={},
            headers={"X-Api-Key": mock_api_key}
        )
        
        assert response.status_code == 422
