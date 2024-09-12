import requests
import streamlit as st

import api_util.workflow_api as w_api


def start_page():

    # st.balloons()
    with st.sidebar:
        # Add workflow selection box
        workflows = w_api.get_all_workflows()
        workflow_options = [f"{workflow['description']} - {workflow['createdBy']}" for workflow in workflows]
        workflow_options.insert(0, "Create new WorkFlow")
        
        selected_workflow = st.sidebar.selectbox("Select Workflow", workflow_options)

    # Application title
    st.title("Create or Update your Workflow")

    employee_id = st.text_input("Input your employee ID", value="")
    workflow_description = st.text_input("Input your workflow description", value="")

    tool_published = st.selectbox(
        "Select tool published status:",
        ('True', 'False')
    )

    # Deploy settings button
    if st.button("Deploy settings"):

        if employee_id != "":
            st.balloons()
            st.success("Settings deployed successfully!")

            if selected_workflow == "Create new WorkFlow":
                # Create a new workflow
                request_body = {
                    'description': workflow_description,
                    'createdBy': employee_id,
                    'toolPublished': tool_published == 'True'
                }
                
                response = w_api.create_workflow(request_body)
                st.write(f"Create response by {employee_id}")
            else:
                # Update existing workflow
                request_body = {
                    'description': workflow_description,
                    'updatedBy': employee_id,
                    'toolPublished': tool_published == 'True'
                }

                selected_workflow_index = workflow_options.index(selected_workflow)
                selected_workflow_id = workflows[selected_workflow_index - 1]['id']
                response = w_api.update_workflow(data=request_body, flowId=selected_workflow_id)
                st.write(f"Update response by {employee_id}")

            st.write(response)

        else:
            st.error("Please fill in all the fields.")

    # Section to delete a workflow
    st.header("Delete a Workflow")

    # Select workflow to delete
    delete_workflow = st.selectbox("Select Workflow to Delete", workflow_options[1:])  # Exclude "Create new WorkFlow"

    # Delete button
    if st.button("Delete selected Workflow"):
        if delete_workflow:
            # Find the workflow ID for deletion
            delete_workflow_index = workflow_options.index(delete_workflow)
            delete_workflow_id = workflows[delete_workflow_index - 1]['id']  # Adjust index since "Create new WorkFlow" is inserted at the beginning

            # Perform deletion
            delete_response = w_api.delete_workflow(flowId=delete_workflow_id)
            st.write(f"Deleted Workflow: {delete_workflow}")
            # st.write(delete_response)
        else:
            st.error("Please select a Workflow to delete.")
