"""Testes para o endpoint de health check."""

from fastapi.testclient import TestClient


class TestHealth:
    """Testes para o endpoint /health."""
    
    def test_health_check(self, client: TestClient):
        """Testa se o health check retorna status healthy."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"