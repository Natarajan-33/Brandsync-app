import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from datetime import datetime
import json

client = TestClient(app)

@pytest.fixture
def mock_sendgrid():
    with patch('app.endpoints.outreach.SendGridAPIClient') as mock_client:
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 202  # SendGrid returns 202 for successful sends
        
        # Configure the mock client to return our mock response
        mock_instance = mock_client.return_value
        mock_instance.send.return_value = mock_response
        
        yield mock_client

@pytest.fixture
def valid_email_payload():
    return {
        "influencer_name": "Test Influencer",
        "influencer_email": "test@example.com",
        "campaign_name": "Test Campaign",
        "message": "This is a test message for our collaboration.",
        "influencer_id": 1,
        "campaign_id": 1
    }

@pytest.fixture
def invalid_email_payload():
    return {
        "influencer_name": "Test Influencer",
        # Missing email field
        "campaign_name": "Test Campaign",
        "message": "This is a test message for our collaboration."
    }

def test_send_email_success(mock_sendgrid, valid_email_payload):
    """Test successful email sending"""
    # Set environment variables for the test
    with patch.dict('os.environ', {
        'SENDGRID_API_KEY': 'test_api_key',
        'DEFAULT_SENDER_EMAIL': 'sender@example.com'
    }):
        response = client.post("/outreach/email", json=valid_email_payload)
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Email sent successfully" in data["message"]
        assert "timestamp" in data
        
        # Verify SendGrid was called correctly
        mock_sendgrid.assert_called_once()
        mock_instance = mock_sendgrid.return_value
        mock_instance.send.assert_called_once()

def test_send_email_missing_fields(invalid_email_payload):
    """Test email sending with missing required fields"""
    response = client.post("/outreach/email", json=invalid_email_payload)
    
    # Check response for validation error
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "detail" in data

def test_send_email_missing_api_key(mock_sendgrid, valid_email_payload):
    """Test email sending with missing API key"""
    # Set empty environment variables for the test
    with patch.dict('os.environ', {
        'SENDGRID_API_KEY': '',
        'DEFAULT_SENDER_EMAIL': 'sender@example.com'
    }):
        response = client.post("/outreach/email", json=valid_email_payload)
        
        # Check response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "SendGrid API key not configured" in data["detail"]

def test_send_email_missing_sender_email(mock_sendgrid, valid_email_payload):
    """Test email sending with missing sender email"""
    # Set environment variables for the test (missing sender email)
    with patch.dict('os.environ', {
        'SENDGRID_API_KEY': 'test_api_key',
        'DEFAULT_SENDER_EMAIL': ''
    }):
        response = client.post("/outreach/email", json=valid_email_payload)
        
        # Check response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Sender email not configured" in data["detail"]

def test_send_email_sendgrid_error(mock_sendgrid, valid_email_payload):
    """Test email sending with SendGrid error"""
    # Configure mock to raise an exception
    mock_instance = mock_sendgrid.return_value
    mock_instance.send.side_effect = Exception("SendGrid API error")
    
    # Set environment variables for the test
    with patch.dict('os.environ', {
        'SENDGRID_API_KEY': 'test_api_key',
        'DEFAULT_SENDER_EMAIL': 'sender@example.com'
    }):
        response = client.post("/outreach/email", json=valid_email_payload)
        
        # Check response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Failed to send email" in data["detail"]


# Fixtures for voice agent tests
@pytest.fixture
def mock_elevenlabs_api():
    with patch('app.endpoints.outreach.requests.post') as mock_post:
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "call_id": "test-call-id-123",
            "status": "initiated"
        }
        
        # Configure the mock to return our mock response
        mock_post.return_value = mock_response
        
        yield mock_post

@pytest.fixture
def valid_voice_payload():
    return {
        "phone_number": "+911234567890",
        "influencer_name": "Priya Sharma",
        "brand_name": "GlowUp Cosmetics",
        "campaign_name": "Diwali Glow Campaign",
        "deliverables": "1 Instagram post, 3 stories, 1 reel",
        "timeline": "2 weeks",
        "budget_range": "$2,000 - $4,000",
        "influencer_id": 1,
        "campaign_id": 1
    }

@pytest.fixture
def invalid_voice_payload():
    return {
        # Missing phone number
        "influencer_name": "Priya Sharma",
        "brand_name": "GlowUp Cosmetics",
        "campaign_name": "Diwali Glow Campaign",
        "deliverables": "1 Instagram post, 3 stories, 1 reel",
        "timeline": "2 weeks",
        "budget_range": "$2,000 - $4,000"
    }

@pytest.fixture
def valid_negotiation_summary():
    return {
        "influencer_name": "Priya Sharma",
        "brand_name": "GlowUp Cosmetics",
        "campaign_name": "Diwali Glow Campaign",
        "deliverables": "1 Instagram post, 3 stories, 1 reel",
        "timeline": "2 weeks",
        "agreed_budget": "$3,500",
        "status": "accepted",
        "notes": "Influencer requested additional $500 for exclusivity, which was agreed upon.",
        "timestamp": datetime.now().isoformat()
    }

def test_voice_agent_success(mock_elevenlabs_api, valid_voice_payload):
    """Test successful voice agent call"""
    # Set environment variables for the test
    with patch.dict('os.environ', {
        'ELEVENLABS_API_KEY': 'test_api_key',
        'ELEVENLABS_AGENT_ID': 'test_agent_id',
        'USE_MOCK_ELEVENLABS': 'false'  # Force actual API call (which we'll mock)
    }):
        response = client.post("/outreach/voice", json=valid_voice_payload)
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Voice call initiated successfully" in data["message"]
        assert data["call_id"] == "test-call-id-123"
        assert "timestamp" in data
        
        # Verify ElevenLabs API was called correctly
        mock_elevenlabs_api.assert_called_once()
        
        # Verify the API was called with the correct arguments
        args, kwargs = mock_elevenlabs_api.call_args
        assert kwargs["url"] == "https://api.elevenlabs.io/v1/voice/agent/call"
        assert kwargs["headers"]["xi-api-key"] == "test_api_key"
        assert kwargs["json"]["agent_id"] == "test_agent_id"
        assert kwargs["json"]["phone_number"] == valid_voice_payload["phone_number"]
        assert "dynamic_variables" in kwargs["json"]
        assert kwargs["json"]["dynamic_variables"]["influencer_name"] == valid_voice_payload["influencer_name"]

def test_voice_agent_missing_fields(invalid_voice_payload):
    """Test voice agent call with missing required fields"""
    response = client.post("/outreach/voice", json=invalid_voice_payload)
    
    # Check response for validation error
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "detail" in data

def test_voice_agent_missing_api_key(mock_elevenlabs_api, valid_voice_payload):
    """Test voice agent call with missing API key"""
    # Set empty environment variables for the test
    with patch.dict('os.environ', {
        'ELEVENLABS_API_KEY': '',
        'ELEVENLABS_AGENT_ID': 'test_agent_id',
        'USE_MOCK_ELEVENLABS': 'false'  # Force actual API call (which we'll mock)
    }):
        response = client.post("/outreach/voice", json=valid_voice_payload)
        
        # Check response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "ElevenLabs API key not configured" in data["detail"]

def test_voice_agent_missing_agent_id(mock_elevenlabs_api, valid_voice_payload):
    """Test voice agent call with missing agent ID"""
    # Set environment variables for the test (missing agent ID)
    with patch.dict('os.environ', {
        'ELEVENLABS_API_KEY': 'test_api_key',
        'ELEVENLABS_AGENT_ID': '',
        'USE_MOCK_ELEVENLABS': 'false'  # Force actual API call (which we'll mock)
    }):
        response = client.post("/outreach/voice", json=valid_voice_payload)
        
        # Check response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "ElevenLabs Agent ID not configured" in data["detail"]

def test_voice_agent_api_error(mock_elevenlabs_api, valid_voice_payload):
    """Test voice agent call with API error"""
    # Configure mock to return an error response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Invalid phone number format"
    mock_elevenlabs_api.return_value = mock_response
    
    # Set environment variables for the test
    with patch.dict('os.environ', {
        'ELEVENLABS_API_KEY': 'test_api_key',
        'ELEVENLABS_AGENT_ID': 'test_agent_id',
        'USE_MOCK_ELEVENLABS': 'false'  # Force actual API call (which we'll mock)
    }):
        response = client.post("/outreach/voice", json=valid_voice_payload)
        
        # Check response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Voice call failed" in data["detail"]

def test_voice_agent_mock_mode(valid_voice_payload):
    """Test voice agent call in mock mode"""
    # Set environment variables for the test
    with patch.dict('os.environ', {
        'USE_MOCK_ELEVENLABS': 'true'  # Force mock mode
    }):
        response = client.post("/outreach/voice", json=valid_voice_payload)
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Voice call initiated successfully" in data["message"]
        assert data["call_id"].startswith("mock-call-id-")
        assert "timestamp" in data

def test_negotiation_summary(valid_negotiation_summary):
    """Test logging a negotiation summary"""
    response = client.post("/outreach/negotiation/summary", json=valid_negotiation_summary)
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["influencer_name"] == valid_negotiation_summary["influencer_name"]
    assert data["brand_name"] == valid_negotiation_summary["brand_name"]
    assert data["status"] == valid_negotiation_summary["status"]
    assert data["agreed_budget"] == valid_negotiation_summary["agreed_budget"]
    assert "timestamp" in data
