import json
import time

import streamlit as st

import api_util.edge_api as edge_api
import api_util.llm_api as llm_api
import api_util.question_classification_api as q_api
import api_util.workflow_api as w_api
from page import start


def LLM_page():
    with st.sidebar:
        # Add workflow selection box
        workflows = w_api.get_all_workflows()
        
        # if not workflows:
        #     if 'redirected' not in st.session_state:
        #         st.error("No workflows found. Redirecting to workflow creation page...")
        #         time.sleep(2)
        #         st.session_state['page'] = 'Start'
        #         st.session_state['redirected'] = True  # 設置已跳轉的標識符
        #         st.rerun()
        # else:
        #     workflow_options = [f"{workflow['description']} - {workflow['createdBy']}" for workflow in workflows]
        #     selected_workflow = st.sidebar.selectbox("Select Workflow", workflow_options)
        #     selected_workflow_index = workflow_options.index(selected_workflow)
        #     selected_workflow = workflows[selected_workflow_index]

        #     st.session_state['selected_workflow'] = selected_workflow
        #     selected_workflowId = selected_workflow["id"]
    
    # if 'redirected' in st.session_state and not workflows:
    #     start.start_page()
    #     return

    # Application title
    st.title("RAG")

    system_id = st.text_input("Input your system ID", value="")

    # Model selection dropdown
    model = st.selectbox("Select Model", ["gpt-3.5-turbo CHAT", "gpt-4.0", "gpt-3.0"])

    # System prompt
    system_prompt = st.text_input("Input your LLM System prompt", value="")
    
    # Upload files
    st.write("Upload your RAG documents")
    upload_embedding_files = st.file_uploader(
        label='Upload your data',
        accept_multiple_files=True,
        type=['txt', 'csv', 'pdf']
    )   

    # Consider about upload multiple files not on one embedded file !!!
    upload_embedding_file = upload_embedding_files[0]
    file_description = st.text_input("Input your LLM settings description", value="")
    file_type = upload_embedding_file.name.split('.')[-1].lower()

    # Deploy settings button
    if st.button("Deploy settings"):
        
        payload = {
                "modelConfig": {"model": model},
                "description": file_description,
                "promptTemplate": {"systemPrompt": system_prompt}
            }

        files = {
            'file': upload_embedding_file,
            'request': (None, json.dumps(payload), 'application/json')
        }

        # Send the request (assuming w_api.create_llm_node exists)
        response = llm_api.create_llm(flowId=selected_workflowId, files=files)
        if response and 'id' in response:
            st.write(f"LLM Node created successfully by {system_id}. Node ID: {response['id']}")
            st.write(response)
            st.session_state["SourceNodeId"] = response['id']
        else:
            st.error("Failed to create LLM Node.")
            return

        w_request_body = {
                'updatedBy': system_id
            }
        w_api.update_workflow(w_request_body, selected_workflowId)
    else:
        pass
        # st.error("No nodes found for the selected workflow.")
