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

def test_vector_search_accuracy(test_client, test_db):
    """Test the accuracy of vector search for document retrieval."""
    # Upload a test document
    test_content = """
    The mitochondria is the powerhouse of the cell.
    It produces energy through cellular respiration.
    ATP is generated in this process.
    """
    test_file = io.BytesIO(test_content.encode())
    test_file.name = "biology.txt"
    
    response = test_client.post(
        "/upload",
        files={"file": (test_file.name, test_file, "text/plain")}
    )
    assert response.status_code == 200
    
    # Test semantic search with relevant query
    chat_request = {
        "message": "What is the role of mitochondria?",
        "history": []
    }
    response = test_client.post("/chat", json=chat_request)
    assert response.status_code == 200
    result = response.json()
    assert "mitochondria" in result["message"].lower()
    assert "powerhouse" in result["message"].lower()
    assert "energy" in result["message"].lower()

def test_flashcard_generation(test_client, test_db):
    """Test automatic flashcard generation from uploaded content."""
    # Upload test content
    test_content = """
    Python is a high-level programming language.
    It was created by Guido van Rossum in 1991.
    Python emphasizes code readability and uses significant whitespace.
    """
    test_file = io.BytesIO(test_content.encode())
    test_file.name = "python_info.txt"
    
    response = test_client.post(
        "/upload",
        files={"file": (test_file.name, test_file, "text/plain")}
    )
    assert response.status_code == 200
    
    # Test flashcard generation
    response = test_client.get("/questions")
    assert response.status_code == 200
    result = response.json()
    questions = result["questions"]
    
    # Verify question quality
    assert len(questions) > 0
    # Check if questions are relevant to the content
    relevant_terms = ["Python", "programming", "Guido", "whitespace"]
    has_relevant_question = any(
        any(term.lower() in q.lower() for term in relevant_terms)
        for q in questions
    )
    assert has_relevant_question

@pytest.mark.snapshot
def test_ai_response_consistency(test_client, test_db, snapshot):
    """Test AI response consistency using snapshots."""
    # Test with a fixed input for consistency
    chat_request = {
        "message": "What are the key features of Python?",
        "history": []
    }
    
    response = test_client.post("/chat", json=chat_request)
    assert response.status_code == 200
    result = response.json()
    
    # Compare with snapshot
    snapshot.assert_match(result["message"])

def test_chat_context_retention(test_client, test_db):
    """Test if the chat maintains context across multiple messages."""
    # First message
    chat_request1 = {
        "message": "What is Python?",
        "history": []
    }
    response1 = test_client.post("/chat", json=chat_request1)
    assert response1.status_code == 200
    
    # Follow-up message with history
    chat_request2 = {
        "message": "What are its main features?",
        "history": [
            {"role": "user", "content": chat_request1["message"]},
            {"role": "assistant", "content": response1.json()["message"]}
        ]
    }
    response2 = test_client.post("/chat", json=chat_request2)
    assert response2.status_code == 200
    result2 = response2.json()
    
    # Verify context retention
    assert "features" in result2["message"].lower()
    assert result2["message"] != response1.json()["message"] 