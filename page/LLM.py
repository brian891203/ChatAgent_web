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
        KMs = llm_api.get_all_km()

        KM_options = [f"{km['fileName']} - {km['uploadedBy']} [{idx}]" for idx, km in enumerate(KMs)]
        KM_options.insert(0, "Create new knowledge")
        selected_km = st.sidebar.selectbox("Select KM", KM_options)
        st.write("You selected:", selected_km)

        print(selected_km)

        if selected_km != "Create new knowledge":
            selected_KM_id = KMs[KM_options.index(selected_km) - 1]['id']
            print(selected_KM_id)

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
    if upload_embedding_files:
        upload_embedding_file = upload_embedding_files[0]
        file_name = upload_embedding_file.name.split('.')[0]
        file_type = upload_embedding_file.name.split('.')[-1].lower()
    else:
        upload_embedding_file = None
        file_name = None
        file_type = None

    file_description = st.text_input("Input your LLM settings description", value="")

    # Deploy settings button
    if st.button("Deploy settings"):

        # Create new KM
        if selected_km == "Create new knowledge":
            if system_id != "" and upload_embedding_files != None:
                payload = {
                        "fileName": file_name,
                        "fileType": file_type,
                        "uploadedBy": system_id,
                        "modelConfig": {"model": model},
                        "description": file_description
                        # "promptTemplate": {"systemPrompt": system_prompt}
                    }

                files = {
                    'file': upload_embedding_file,
                    'request': (None, json.dumps(payload), 'application/json')
                }

                response = llm_api.create_llm(files=files)
                if response and 'id' in response:
                    st.write(f"LLM Node created successfully by {system_id}. Node ID: {response['id']}")
                    st.write(response)
                    st.session_state["CreatedKMId"] = response['id']
                else:
                    st.error("Failed to create KM.")
                    return
            else:
                st.error("Please fill in all the fields.")
        
        # Update existing KM
        else:
            if system_id != "":
                payload = {
                        "fileName": file_name,
                        "fileType": file_type,
                        "uploadedBy": system_id,
                        "modelConfig": {"model": model},
                        "description": file_description
                        # "promptTemplate": {"systemPrompt": system_prompt}
                    }

                files = {
                    'file': upload_embedding_file,
                    'request': (None, json.dumps(payload), 'application/json')
                }

                response = llm_api.update_km(kmId=selected_KM_id, files=files)
                if response and 'id' in response:
                    st.write(f"LLM Node updated successfully by {system_id}. Node ID: {response['id']}")
                    st.write(response)
                    st.session_state["UpdatedKMId"] = response['id']
                else:
                    st.error("Failed to update KM.")
                    return
            else:
                st.error("Please fill in your system ID.")
    else:
        pass
        # st.error("No nodes found for the selected workflow.")

    st.header("Delete a KM")
    delete_km = st.selectbox('Select KM to delete', KM_options[1:])

    if st.button('Delete selected KM'):
        if delete_km:
            delete_km_index = KM_options.index(delete_km)
            delete_km_id = KMs[delete_km_index - 1]['id']

            delete_response = llm_api.delete_km(kmId=delete_km_id)
            st.write(f"Deleted KM: {delete_km}")
            st.write(delete_response)
        else:
            st.error("Please select a KM to delete.")
