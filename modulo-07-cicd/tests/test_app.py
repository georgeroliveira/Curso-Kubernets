import pytest
import sys
import os

# Adiciona o diretório pai ao path para importar o app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Testa se a rota /health retorna 200 e o formato correto"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    # Aceita 'healthy' ou status simulado dependendo do estágio do lab
    assert data['status'] in ['healthy', 'ok', 'unhealthy']

def test_index_route_redirect(client):
    """Testa se a home page responde (pode ser 200 ou redirect se não autenticado/configurado)"""
    response = client.get('/')
    assert response.status_code in [200, 302]