import requests

BASE_URL = "http://localhost:8080/AflowGent/v1/workflows"

# Create an edge
def create_edge(flowId, data):
    url = f"{BASE_URL}/{flowId}/edges"
    response = requests.post(url, json=data)
    return response.json()

# Get edge by ID
def get_edge_by_id(flowId, edgeId):
    url = f"{BASE_URL}/{flowId}/edges/{edgeId}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
