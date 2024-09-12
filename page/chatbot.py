import json
import time

import requests
import streamlit as st


def chatbot():
    """
    A simple chatbot using Azure OpenAI.

    This chatbot interacts with the user by sending messages to Azure OpenAI service and displaying the responses.

    Usage:
        1. Enter a message in the chat input box.
        2. The message will be sent to Azure OpenAI service for processing.
        3. The response from the service will be displayed in the chat.

    Dependencies:
        - streamlit
        - requests
        - json
    """

    st.title("GPT-with Azure OpenAI")

    # Azure OpenAI service URL and API key
    azure_openai_url = "https://api-csd-lab-je.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
    api_key = "2933c0c5028844ac83b5071171cb9a5f"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Build request payload
            payload = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}]
            }

            # Send request to Azure OpenAI service
            headers = {
                "Content-Type": "application/json",
                "api-key": api_key
            }
            response = requests.post(azure_openai_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                response_content = ""
                try:
                    response_data = response.json()
                    for message_obj in response_data.get("choices", []):
                        if "message" in message_obj:
                            response_content += message_obj["message"]["content"] + " "

                            # Remove extra spaces
                            response_content = response_content.strip()
                            
                    # Display the merged response content
                    message_placeholder = st.empty()
                    content = ""
                    for text in response_content.split():
                        content += text + " "
                        message_placeholder.markdown(content)
                        time.sleep(0.07)
                    # st.markdown(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
    
                except json.JSONDecodeError as e:
                    st.error(f"JSON decode error: {e.msg}")
                    st.write("Raw response:", response.text)
            else:
                st.error("Failed to get response from Azure OpenAI service: " + response.json().get("error", "Unknown error"))

if __name__ == "__main__":
    chatbot()
