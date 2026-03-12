"""
Testes para a rota /health
"""


class TestHealth:
    """Testes da rota GET /health"""
    
    def test_health_check_returns_200(self, test_client):
        """Teste básico - health check deve retornar 200."""
        response = test_client.get("/api/v1/health")
        
        assert response.status_code == 200
    
    def test_health_check_returns_healthy(self, test_client):
        """Teste do conteúdo - deve retornar 'healthy'."""
        response = test_client.get("/api/v1/health")
        
        assert response.status_code == 200
        assert response.json() == "healthy"
    
    def test_health_check_no_auth_required(self, test_client):
        """Teste que health check não requer autenticação."""
        # Não passa nenhum header de autenticação
        response = test_client.get("/api/v1/health")
        
        assert response.status_code == 200
        assert response.json() == "healthy"
