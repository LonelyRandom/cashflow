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

    st.markdown("""
    <style>                
    /* ================= MOBILE ================= */
    @media (max-width: 767px) {
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100vh !important;
            width: 100vw !important;
            max-width: 100vw !important;
            transform: translateX(-100%);
            transition: transform 0.3s ease-in-out;
            z-index: 999999 !important;
        }

        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
        }

        .stSidebarCollapseButton button {
            position: fixed !important;
            top: 10px !important;
            right: 10px !important;
            z-index: 1000000 !important;
            font-size: 24px !important;
            padding: 14px !important;
            background: rgba(0,0,0,0.1) !important;
            border-radius: 50% !important;
        }

        .main .block-container {
            padding: 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)