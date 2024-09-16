import requests


# Create llm
def create_llm(files):
    url = "http://localhost:8080/ChatAgent/v1/knowledges"
    response = requests.post(url, files=files)
    return response.json()

def get_all_km():
    url = "http://localhost:8080/ChatAgent/v1/knowledges/all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def update_km(kmId, files):
    url = f"http://localhost:8080/ChatAgent/v1/knowledges/{kmId}"
    response = requests.put(url, files=files)
    return response.json()

def delete_km(kmId):
    url = f"http://localhost:8080/ChatAgent/v1/knowledges/{kmId}"
    response = requests.delete(url)
    return response

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