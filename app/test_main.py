import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from .main import app
import os
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_env():
    """Fixture para establecer variables de entorno de prueba."""
    os.environ["OPENAI_API_KEY"] = "sk-test-key-123"
    yield
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

@pytest_asyncio.fixture
async def async_client():
    """Fixture to create a FastAPI test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_chat_endpoint(async_client: AsyncClient):
    """Prueba del endpoint /chat."""
    # Mock de la respuesta de OpenAI
    mock_response = type('obj', (object,), {'content': 'Respuesta de prueba'})
    
    with patch('langchain_openai.ChatOpenAI.invoke', return_value=mock_response):
        # Preparar el mensaje de prueba
        test_message = {"user_message": "Hola, ¿cómo estás?"}
        
        # Realizar la petición POST
        response = await async_client.post("/chat", json=test_message)
        
        # Verificar la respuesta
        assert response.status_code == 200
        assert "assistant_message" in response.json()