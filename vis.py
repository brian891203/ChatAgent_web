import os

import streamlit as st

from page import LLM, Home, chatbot, question_classification, sidebar, start


def main():
    """
    Main is responsible for the visualisation of everything connected with streamlit.
    It is the web application itself.
    """
    
    # Sets sidebar's header and logo
    sidebar.sidebar_head()

    # 檢查並設置 session_state 儲存頁面狀態
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Home Page'

    # 使用選擇框來改變頁面（這一部分應該放在邏輯後面，以避免覆蓋 session_state）
    node_type = st.sidebar.selectbox("Analysis type", ['Home Page', 'Start', 'Question Classifier','LLM', 'Chatbot', 'Answer'])

    # 檢查 node_type 是否與 session_state['page'] 不同，如果不同則更新 session_state
    if node_type != st.session_state['page']:
        st.session_state['page'] = node_type
        st.rerun()

    # 根據 session_state 中的 page 值決定顯示的頁面
    if st.session_state['page'] == 'Home Page':
        Home.home_page()
    elif st.session_state['page'] == 'Start':
        start.start_page()
    elif st.session_state['page'] == 'Question Classifier':
        question_classification.question_classification_page()
    elif st.session_state['page'] == 'Chatbot':
        chatbot.chatbot()
    elif st.session_state['page'] == 'LLM':
        LLM.LLM_page()
    elif st.session_state['page'] == 'Answer':
        pass

if __name__ == '__main__':
    main()
