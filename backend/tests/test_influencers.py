import sys
import os
import pytest
from fastapi.testclient import TestClient

# Import and initialize the influencers module manually
from app.endpoints import influencers

# Import the app after initializing the influencers module
from app.main import app

# Initialize the vector database for testing
influencers.initialize_vector_db()

# Create test client
client = TestClient(app)

def test_get_all_influencers():
    """Test the GET /influencers/ endpoint"""
    response = client.get("/influencers/")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    influencers = response.json()
    assert isinstance(influencers, list)
    assert len(influencers) >= 5  # We should have at least 5 influencers
    
    # Check first influencer has all required fields
    first_influencer = influencers[0]
    required_fields = ["id", "name", "platforms", "category", "followers", 
                      "engagement_rate", "region", "rate_card", "contact"]
    
    for field in required_fields:
        assert field in first_influencer

def test_search_influencers():
    """Test the GET /influencers/search endpoint"""
    # Test with a specific query
    response = client.get("/influencers/search?q=fashion influencers in India")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    results = response.json()
    assert isinstance(results, list)
    
    # We should get some results (not checking exact matches as it depends on embeddings)
    assert len(results) > 0
    
    # Check that each result has the required fields
    for influencer in results:
        required_fields = ["id", "name", "platforms", "category", "followers", 
                          "engagement_rate", "region", "rate_card", "contact"]
        
        for field in required_fields:
            assert field in influencer

def test_search_influencers_tech():
    """Test the search endpoint with a tech-related query"""
    response = client.get("/influencers/search?q=tech influencers with YouTube presence")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    results = response.json()
    assert isinstance(results, list)
    assert len(results) > 0
