import time

import streamlit as st

import api_util.edge_api as edge_api
import api_util.question_classification_api as q_api
import api_util.workflow_api as w_api
from page import start


def question_classification_page():

    with st.sidebar:
        # Add workflow selection box
        workflows = w_api.get_all_workflows()
        
        if not workflows:
            if 'redirected' not in st.session_state:
                st.error("No workflows found. Redirecting to workflow creation page...")
                time.sleep(2)
                st.session_state['page'] = 'Start'
                st.session_state['redirected'] = True  # 設置已跳轉的標識符
                st.rerun()
        else:
            workflow_options = [f"{workflow['description']} - {workflow['createdBy']}" for workflow in workflows]
            selected_workflow = st.sidebar.selectbox("Select Workflow", workflow_options)
            selected_workflow_index = workflow_options.index(selected_workflow)
            selected_workflow = workflows[selected_workflow_index]

            st.session_state['selected_workflow'] = selected_workflow
            selected_workflowId = selected_workflow["id"]

            # files = st.sidebar.file_uploader(label='Upload your data',
            #                                 accept_multiple_files=True,
            #                                 type=['txt', 'csv', 'pdf'])
    
    if 'redirected' in st.session_state and not workflows:
        start.start_page()
        return

    # Application title
    st.title("Question Classifier")

    employee_id = st.text_input("Input your employee ID", value="")

    # Model selection dropdown
    model = st.selectbox("Select Model", ["gpt-3.5-turbo CHAT", "gpt-4.0", "gpt-3.0"])

    Question_title = st.text_input("Input your Question title", value="")

    # Initialize category count and input boxes
    if 'category_count' not in st.session_state:
        st.session_state['category_count'] = 2

    # Render input boxes based on current category count
    for i in range(1, st.session_state['category_count'] + 1):
        st.markdown(f"#### Category {i}")
        st.text_input(f"LLM classification description {i}", key=f"category_{i}")

    # Add and Remove category buttons directly below each other
    if st.button("Add Category", key='add_button_below'):
        st.session_state['category_count'] += 1
        st.rerun()

    if st.button("Remove Category", key='remove_button_below'):
        if st.session_state['category_count'] > 1:
            st.session_state['category_count'] -= 1
            st.rerun()
        else:
            st.warning("At least one category is required.")

    # Explanation text
    st.markdown("Define the classification conditions of user questions, LLM can define how the conversation progresses based on the classification description.")

    # Deploy settings button
    if st.button("Deploy settings"):
        classes_data = {}
        for i in range(1, st.session_state['category_count'] + 1):
            classes_data[f"category_{i}"] = st.session_state.get(f"category_{i}", "")

        if all(value for value in classes_data.values()) and (employee_id != ""):
            st.balloons()
            st.success("Settings deployed successfully!")

            q_request_body = {
                'title': Question_title,
                'description': Question_title,
                'classes': classes_data
            }
            # st.write(q_request_body)

            response = q_api.create_QuestionCategory(q_request_body, selected_workflowId)
            if response and 'id' in response:
                st.write(f"Question Classifier Node created successfully by {employee_id}. Node ID: {response['id']}")
                st.write(response)
                st.session_state["SourceNodeId"] = response['id']
            else:
                st.error("Failed to create Question Classifier Node.")
                return
            
            w_request_body = {
                'updatedBy': employee_id
            }
            w_api.update_workflow(w_request_body, selected_workflowId)

        else:
            st.error("Please fill in all the fields.")

    # Get all node information by workflow ID
    st.header("Create Edges")
    nodes_info = w_api.get_all_node_info_by_workflow_id(selected_workflowId)
    if nodes_info:
        # Prepare the select box options
        node_options = [
            f"{node['type']} - {node['description']} (ID: {node['id']})"
            for node in nodes_info
        ]
        selected_node = st.selectbox("Select Target Node", node_options)

        selected_target_node_id = selected_node.split("(ID: ")[1].rstrip(")")

        # Create Edge Button
        if st.button("Create Edge"):
            if 'SourceNodeId' in st.session_state:
                edge_payload = {
                    "sourceNodeId": st.session_state["SourceNodeId"],
                    "targetNodeId": selected_target_node_id
                }
                edge_response = edge_api.create_edge(flowId=selected_workflowId, data=edge_payload)
                st.write("Edge created:", edge_response)
            else:
                st.error("Source Node ID not found.")
    else:
        st.error("No nodes found for the selected workflow.")
