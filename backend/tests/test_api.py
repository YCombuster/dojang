import pytest
from fastapi.testclient import TestClient

def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_endpoint(test_client):
    """Test the document upload endpoint."""
    # Add this test once the upload endpoint is implemented
    pass

def test_chat_endpoint(test_client):
    """Test the chat endpoint."""
    # Add this test once the chat endpoint is implemented
    pass

def test_questions_endpoint(test_client):
    """Test the questions endpoint."""
    # Add this test once the questions endpoint is implemented
    pass 