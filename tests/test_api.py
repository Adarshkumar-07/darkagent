from fastapi.testclient import TestClient
from backend.main import app

def test_health(): assert TestClient(app).get('/health').json() == {'status':'ok'}
def test_validation_rejects_empty(): assert TestClient(app).post('/api/chat',json={'message':' ','conversation':[]}).status_code == 422
def test_validation_rejects_extra_fields(): assert TestClient(app).post('/api/chat',json={'message':'hello','unexpected':True}).status_code == 422
