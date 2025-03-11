import pytest
import json
import io
from fastapi.testclient import TestClient

def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_endpoint(test_client, test_db):
    """Test the document upload endpoint."""
    # Create a test file
    test_file = io.BytesIO(b"This is a test document for studying.")
    test_file.name = "test_document.pdf"
    
    # Test file upload
    response = test_client.post(
        "/upload",
        files={"file": (test_file.name, test_file, "application/pdf")}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "message" in result

def test_chat_endpoint(test_client, test_db):
    """Test the chat endpoint."""
    # Test chat request
    chat_request = {
        "message": "What is the main topic of the document?",
        "history": []
    }
    
    response = test_client.post(
        "/chat",
        json=chat_request
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "message" in result

def test_questions_endpoint(test_client, test_db):
    """Test the questions endpoint."""
    response = test_client.get("/questions")
    
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert "questions" in result
    assert isinstance(result["questions"], list)
    
def test_invalid_upload(test_client):
    """Test upload endpoint with invalid file."""
    response = test_client.post("/upload", files={})
    assert response.status_code in [400, 422]  # Either bad request or unprocessable entity

def test_invalid_chat_request(test_client):
    """Test chat endpoint with invalid request."""
    response = test_client.post("/chat", json={})
    assert response.status_code in [400, 422] 