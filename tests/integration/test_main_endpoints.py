"""
Testes de integração para endpoints principais
"""
import pytest
from fastapi.testclient import TestClient


class TestMainEndpoints:
    """Testes para endpoints principais da API"""
    
    def test_root_endpoint_success(self, client):
        """Testa endpoint raiz com sucesso"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estrutura da resposta
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        
        # Verificar valores
        assert data["message"] == "Coffee Shop API"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
    
    def test_root_endpoint_response_format(self, client):
        """Testa formato da resposta do endpoint raiz"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar tipos dos campos
        assert isinstance(data["message"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["docs"], str)
        
        # Verificar se os valores não estão vazios
        assert data["message"] != ""
        assert data["version"] != ""
        assert data["docs"] != ""
    
    def test_health_endpoint_success(self, client):
        """Testa endpoint de health check com sucesso"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estrutura da resposta
        assert "status" in data
        
        # Verificar valor
        assert data["status"] == "healthy"
    
    def test_health_endpoint_response_format(self, client):
        """Testa formato da resposta do endpoint de health check"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar tipo do campo
        assert isinstance(data["status"], str)
        
        # Verificar se o valor não está vazio
        assert data["status"] != ""
    
    def test_health_endpoint_consistency(self, client):
        """Testa consistência do endpoint de health check"""
        # Fazer múltiplas requisições para verificar consistência
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    def test_root_endpoint_consistency(self, client):
        """Testa consistência do endpoint raiz"""
        # Fazer múltiplas requisições para verificar consistência
        for _ in range(5):
            response = client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Coffee Shop API"
            assert data["version"] == "1.0.0"
            assert data["docs"] == "/docs"
    
    def test_endpoints_headers(self, client):
        """Testa headers das respostas dos endpoints principais"""
        # Testar endpoint raiz
        response = client.get("/")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
        
        # Testar endpoint de health check
        response = client.get("/health")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
    
    def test_endpoints_method_not_allowed(self, client):
        """Testa métodos não permitidos nos endpoints principais"""
        # Testar POST no endpoint raiz
        response = client.post("/")
        assert response.status_code == 405  # Method Not Allowed
        
        # Testar POST no endpoint de health check
        response = client.post("/health")
        assert response.status_code == 405  # Method Not Allowed
        
        # Testar PUT no endpoint raiz
        response = client.put("/")
        assert response.status_code == 405  # Method Not Allowed
        
        # Testar DELETE no endpoint de health check
        response = client.delete("/health")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_endpoints_with_different_headers(self, client):
        """Testa endpoints com diferentes headers"""
        # Testar com header Accept
        response = client.get("/", headers={"Accept": "application/json"})
        assert response.status_code == 200
        
        # Testar com header Accept diferente
        response = client.get("/", headers={"Accept": "*/*"})
        assert response.status_code == 200
        
        # Testar endpoint de health check com diferentes headers
        response = client.get("/health", headers={"Accept": "application/json"})
        assert response.status_code == 200
        
        response = client.get("/health", headers={"Accept": "*/*"})
        assert response.status_code == 200


