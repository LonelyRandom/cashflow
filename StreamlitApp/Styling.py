import streamlit as st


def styling():
    st.markdown(
    f"""
        <style>
        [class*="st-key-debt-btn-info-"] button {{
            height: 99px !important;
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
            height: 97px;
            padding: 5px;
            margin-bottom: -100px;
            background-color: rgb(43, 44, 54);
        }} 
        [class*="st-key-navbar-fund-info-"] {{
            text-align: center !important;
            border: 1px solid rgba(250, 250, 250, 0.2);
            border-radius: 10px;
            padding: 12px;
        }}
        [class*="st-key-log-info-"] {{
            text-align: center !important;
            border: 1px solid rgba(250, 250, 250, 0.2);
            border-radius: 10px;
            padding: 12px;
        }}
        </style>
    """, unsafe_allow_html=True)