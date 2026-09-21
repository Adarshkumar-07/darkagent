from fastapi.testclient import TestClient
from backend.main import app

def test_health():
    assert TestClient(app).get('/health').json() == {'status': 'ok'}

def test_validation_rejects_empty_and_extra_fields():
    client = TestClient(app)
    assert client.post('/api/chat', json={'message': ' ', 'conversation': []}).status_code == 422
    assert client.post('/api/chat', json={'message': 'hello', 'unexpected': True}).status_code == 422

def test_chat_response_is_safe_without_provider(monkeypatch):
    from backend.routes import chat as route
    monkeypatch.setattr(route.service, 'generate_reply', lambda message, conversation: 'Hello from test')
    response = TestClient(app).post('/api/chat', json={'message': 'hello', 'conversation': []})
    assert response.status_code == 200
    assert response.json()['reply'] == 'Hello from test'
    assert len(response.json()['conversation']) == 2
