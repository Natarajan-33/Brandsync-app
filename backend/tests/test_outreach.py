import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from datetime import datetime

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
