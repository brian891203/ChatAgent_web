import requests

BASE_URL = "http://localhost:8080/ChatAgent/v1/chat"

def create_query(kmId, data):
    url = f"{BASE_URL}/{kmId}/execute"
    response = requests.post(url, json=data)
    return response.json()
