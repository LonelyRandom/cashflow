import streamlit as st


def styling():
    st.markdown(
    f"""
        <style>
        .st-key-debt-eye button{{
            height: 70px;
            padding: 5px;
            margin-bottom: -100px;
        }}  
        .st-key-debt-detail button{{
            height: 70px;
            padding: 5px;
            margin-bottom: -100px;
        }}  
        .st-key-lend-eye button{{
            height: 70px;
            padding: 5px;
            margin-bottom: -100px;
        }}  
        .st-key-lend-detail button{{
            height: 70px;
            padding: 5px;
            margin-bottom: -100px;
        }}  
        [class*="st-key-debt-btn-info-"] button {{
            height: 99px !important;
            padding: 5px !important;
            margin-bottom: -100px !important;
        }}
        [class*="st-key-show-eye-"] button {{
            height: 70px !important;
            padding: 5px !important;
            margin-bottom: -100px !important;
        }}
        [class*="st-key-choose-ref-"] button {{
            height: 99px !important;
            padding: 5px !important;
            margin-bottom: -100px !important;
        }}
        .st-key-film-navbar {{
            background-color: #1D546D;
            padding: 5px;
            border-radius: 10px;
        }}
        [class*="st-key-edit_log_"] button{{
            height: 100px;
            padding: 5px;
            margin-bottom: -100px;
        }}  
        </style>
        </style>
    """, unsafe_allow_html=True)