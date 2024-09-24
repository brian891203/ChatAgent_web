import time

import requests
import streamlit as st

from api_util import chat_api, llm_api


def chatbot():
    with st.sidebar:
        # Add workflow selection box
        KMs = llm_api.get_all_km()
        KM_options = [f"{km['description']} - {km['uploadedBy']} [{idx}]" for idx, km in enumerate(KMs)]
        selected_km = st.sidebar.selectbox("Select KM", KM_options)
        st.write("You selected:", selected_km)
        selected_KM_id = KMs[KM_options.index(selected_km)]['id']

    st.title("Chatbot")

    # Initialize the conversation history in session state if not already there
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display previous messages from history
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Text input for user prompt
    if user_input := st.chat_input("Ask me anything..."):
        # Append the user's message to the session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message in the chat
        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare the backend request with the selected KM ID and user input
        request_body = {
            "query": user_input
        }

        print(request_body)

        # Call the backend API to get the response
        backend_response = chat_api.create_query(selected_KM_id, request_body)
        print(backend_response)

        # Extract the assistant's answer from the response
        if 'answer' in backend_response:
            answer = backend_response['answer']
            
            # Simulate streaming response by splitting the answer into individual characters
            with st.chat_message("assistant"):
                message_placeholder = st.empty()  # Placeholder for the message
                full_response = ""
                for char in answer:
                    full_response += char
                    message_placeholder.markdown(full_response)
                    time.sleep(0.05)  # Adjust the delay for the streaming effect

            # Append the full assistant's message to the session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})


# Run the chatbot
if __name__ == "__main__":
    chatbot()
