import base64

import streamlit as st

# from vis_helpers import vis_utils
# from constants import LABELS

def sidebar_head():
    """
    Sets Page title, page icon, layout, initial_sidebar_state
    Sets position of radiobuttons (in a row or one beneath another)
    Shows logo in the sidebar
    """
    # st.set_page_config(
    #     page_title="國泰金控 | AFlowGent",
    #     page_icon="./img/icon.png",
    #     layout="wide",
    #     initial_sidebar_state="auto"
    # )

    # st.set_option('deprecation.showfileUploaderEncoding', False)

    # SERSitivis logo
    html_code = show_logo(100, [1, 1, 1, 1], margin=[0, 0, 0, 0])
    st.sidebar.markdown(html_code, unsafe_allow_html=True)
    st.sidebar.markdown('')
    st.sidebar.markdown('')

@st.cache_resource
def show_logo(width, padding, margin):
    padding_top, padding_right, padding_bottom, padding_left = padding
    margin_top, margin_right, margin_bottom, margin_left = margin
    
    # link = 'http://localhost:8501/'
    
    with open('./img/logo.png', 'rb') as f:
        data = f.read()
    
    bin_str = base64.b64encode(data).decode()
    html_code = f'''
                <img src="data:image/png;base64,{bin_str}"
                style="
                     margin: auto;
                     width: {width}%;
                     margin-top: {margin_top}px;
                     margin-right: {margin_right}px;
                     margin-bottom: {margin_bottom}px;
                     margin-left: {margin_left}%;
                     padding-top: {margin_top}px;
                     padding-right: {padding_right}px;
                     padding-bottom: {padding_bottom}px;
                     padding-left: {padding_left}%;
                     "/>
                '''

    return html_code



# def print_widget_labels(widget_title, margin_top=5, margin_bottom=10):
#     """
#     Prints Widget label on the sidebar and lets adjust its margins easily
#     :param widget_title: Str
#     """
#     st.sidebar.markdown(
#         f"""<p style="font-weight:500; margin-top:{margin_top}px;margin-bottom:{margin_bottom}px">{widget_title}</p>""",
#         unsafe_allow_html=True)


# def choose_spectra_type():
#     spectra_types = ['EMPTY', 'BWTEK', 'RENI', 'WITEC', 'WASATCH', 'TELEDYNE', 'JOBIN']
#     spectrometer = st.sidebar.selectbox(
#         "Spectra type",
#         spectra_types,
#         format_func=LABELS.get,
#         index=0)
#     return spectrometer