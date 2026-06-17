import gspread
from google.oauth2.service_account import Credentials#
import streamlit as st
import pandas as pd

@st.cache_resource
def get_gsheet_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["connections"]["gsheets"],
        scopes=scope
    )

    return gspread.authorize(creds)

@st.cache_resource()
def log_worksheet():
    client = get_gsheet_client()

    spreadsheet = client.open(
        st.secrets["indicators"]["SPREAD"]
    )

    worksheet = spreadsheet.worksheet(
        st.secrets["indicators"]["USER_LOG"]
    )

    return worksheet

def load_data_log():
    try:
        log_data = log_worksheet().get_all_records()
        df = pd.DataFrame(log_data)
        if df.empty:
            return pd.DataFrame(columns=['Timestamp', 'Fund', 'Category', 'Amount', 'Notes'])
        else:
            return df
    
    except Exception as e:
        return pd.DataFrame(columns=['Timestamp', 'Fund', 'Category', 'Amount', 'Notes'])

@st.cache_resource()
def fund_worksheet():
    client = get_gsheet_client()

    spreadsheet = client.open(
        st.secrets["indicators"]["SPREAD"]
    )

    worksheet = spreadsheet.worksheet(
        st.secrets["indicators"]["USER_FUND"]
    )

    return worksheet

def load_data_fund():
    try:
        fund_data = fund_worksheet().get_all_records()
        df = pd.DataFrame(fund_data)

        if df.empty:
            return pd.DataFrame(columns=['Type', 'Balance', 'Except Category'])
        else:
            return df
    except Exception as e:
        return pd.DataFrame(columns=['Type', 'Balance', 'Except Category'])

@st.cache_resource()
def category_worksheet():
    client = get_gsheet_client()

    spreadsheet = client.open(
        st.secrets["indicators"]["SPREAD"]
    )

    worksheet = spreadsheet.worksheet(
        st.secrets["indicators"]["USER_CATEGORY"]
    )

    return worksheet

def load_data_category():
    try:
        category_data = category_worksheet().get_all_records()
        df = pd.DataFrame(category_data)
        if df.empty:
            return pd.DataFrame(columns=['Category', 'Default Value', 'Type'])
        else:
            return df
    
    except Exception as e:
        return pd.DataFrame(columns=['Category', 'Default Value', 'Type'])

@st.cache_resource()
def quick_log_worksheet():
    client = get_gsheet_client()

    spreadsheet = client.open(
        st.secrets["indicators"]["SPREAD"]
    )

    worksheet = spreadsheet.worksheet(
        st.secrets["indicators"]["USER_QUICK_LOG"]
    )

    return worksheet

def load_data_quick_log():
    try:
        quick_log_data = quick_log_worksheet().get_all_records()
        df = pd.DataFrame(quick_log_data)
        if df.empty:
            return pd.DataFrame(columns=['Label', 'Fund', 'Category', 'Amount', 'Notes'])
        else:
            return df
    
    except Exception as e:
        return pd.DataFrame(columns=['Label', 'Fund', 'Category', 'Amount', 'Notes'])