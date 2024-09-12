import requests


# Create llm
def create_llm(flowId, files):
    url = f"http://localhost:8080/AflowGent/v1/workflows/{flowId}/LLM"
    response = requests.post(url, files=files)
    return response.json()

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