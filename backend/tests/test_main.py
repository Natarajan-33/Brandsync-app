import pytest
from fastapi.testclient import TestClient

# Import and initialize the influencers module manually
from app.endpoints import influencers

# Import the app after initializing the influencers module
from app.main import app

# Create test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response content
    data = response.json()
    assert "message" in data
    assert "Welcome to BrandSync API" in data["message"]

def test_api_docs_available():
    """Test that the API documentation is available"""
    response = client.get("/docs")
    
    # Check status code
    assert response.status_code == 200
    
    # Check that the response contains OpenAPI documentation
    assert "text/html" in response.headers["content-type"]
    assert "swagger" in response.text.lower()
