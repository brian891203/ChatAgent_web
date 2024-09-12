import requests

BASE_URL = "http://localhost:8080/AflowGent/v1/workflows"

# Create question category
def create_workflow(data):
    url = BASE_URL  # Replace with your backend API URL
    response = requests.post(url, json=data)
    return response.json()

def get_all_workflows():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def update_workflow(data, flowId):
    url = BASE_URL + f"/{flowId}"
    response = requests.put(url, json=data)
    return response.json()

def delete_workflow(flowId):
    url = BASE_URL + f"/{flowId}"
    response = requests.delete(url)
    return response

def get_all_node_ids_by_workflow_id(workflow_id):
    url = f"{BASE_URL}/{workflow_id}/nodes/ids"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
def get_all_node_info_by_workflow_id(workflow_id):
    url = f"{BASE_URL}/{workflow_id}/nodes/info"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []
    
# # Get question category by employee ID
# def get_QuestionCategory(employee_id):
#     url = GET_BY_EMPID_URL + "/" + employee_id  # Replace with your backend API URL
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
    
#     return response.json()

# #Update question category by employee ID
# def update_QuestionCategory(employee_id, data):
#     url = PUT_URL + "/" + employee_id  # Replace with your backend API URL
#     response = requests.put(url, json=data)
#     return response.json()