import streamlit as st
import graphviz as gv

def home_page():
    """
    Creates and displays a workflow diagram using graphviz in Streamlit.
    """
    # Sidebar content (currently empty)
    with st.sidebar:
        pass

    # Main page title and caption
    st.title(f''':rainbow[{"💬 AFlowGent"}]''')
    st.caption(f''':rainbow[{"🚀 Create your AI agent by work flow patterns"}]''')

    st.subheader("Workflow Diagram")
    # Define the graph using graphviz with horizontal layout
    dot = gv.Digraph(comment='Flowchart')
    dot.attr(rankdir='LR')  # Set the direction from Left to Right

    # Define nodes with styles
    dot.node('A', '起點', shape='ellipse', style='filled', color='lightblue')
    dot.node('B', '分類', shape='box', style='filled', color='lightblue')
    dot.node('C', '請假相關', shape='box', style='filled', color='lightblue')
    dot.node('D', '公文相關', shape='box', style='filled', color='lightblue')
    dot.node('E', '其他問題', shape='box', style='filled', color='lightblue')
    dot.node('F', '請假知識庫', shape='box', style='filled', color='lightblue')
    dot.node('G', '公文知識庫', shape='box', style='filled', color='lightblue')
    dot.node('H', '直接回覆: 你的問題我無法處理', shape='box', style='filled', color='lightblue')
    dot.node('I', '回覆解答', shape='box', style='filled', color='lightblue')
    dot.node('J', '執行請假', shape='box', style='filled', color='lightblue')
    dot.node('K', '回覆解答', shape='box', style='filled', color='lightblue')

    # Define edges with styles
    dot.edge('A', 'B', color='lightgrey')
    dot.edge('B', 'C', color='lightgrey')
    dot.edge('B', 'D', color='lightgrey')
    dot.edge('B', 'E', color='lightgrey')
    dot.edge('C', 'F', color='lightgrey')
    dot.edge('D', 'G', color='lightgrey')
    dot.edge('E', 'H', color='lightgrey')
    dot.edge('F', 'I', color='lightgrey')
    dot.edge('F', 'J', color='lightgrey')
    dot.edge('G', 'K', color='lightgrey')

    # Render the graph to a string
    graph_str = dot.source

    # Display the graph in Streamlit
    st.graphviz_chart(graph_str)

if __name__ == '__main__':
    home_page()
