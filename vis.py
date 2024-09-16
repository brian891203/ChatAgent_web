import os

import streamlit as st

from page import LLM, Home, chatbot, question_classification, sidebar, start


def main():
    """
    Main is responsible for the visualisation of everything connected with streamlit.
    It is the web application itself.
    """
    # 設置頁面標題和圖示
    st.set_page_config(
        page_title="ChatAgent",
        page_icon="./img/icon.png"
    )
    # 設置 sidebar 的 header 和 logo
    sidebar.sidebar_head()
    
    # 檢查是否訪問的是 /admin 路徑
    if 'admin' in st.query_params and st.query_params['admin'] == 'true':
        LLM.LLM_page()

    else:
        # 檢查並設置 session_state 儲存頁面狀態
        if 'page' not in st.session_state:
            st.session_state['page'] = 'Home Page'

        # 使用選擇框來改變頁面（這一部分應該放在邏輯後面，以避免覆蓋 session_state）
        node_type = st.sidebar.selectbox("Analysis type", ['Home Page', 'Chatbot'])

        # 檢查 node_type 是否與 session_state['page'] 不同，如果不同則更新 session_state
        if node_type != st.session_state['page']:
            st.session_state['page'] = node_type
            st.rerun()

        # 根據 session_state 中的 page 值決定顯示的頁面
        if st.session_state['page'] == 'Home Page':
            Home.home_page()
        elif st.session_state['page'] == 'Chatbot':
            chatbot.chatbot()

if __name__ == '__main__':
    main()
