import streamlit as st
from datetime import datetime, date
import time
import re
import pandas as pd
# from value_handling import values_handling
from dateutil.relativedelta import relativedelta
from streamlit_scroll_to_top import scroll_to_here
from Data import load_data_category, load_data_fund, load_data_log, log_worksheet, load_data_quick_log, category_worksheet, fund_worksheet, quick_log_worksheet
import string
from bs4 import BeautifulSoup
from streamlit_float import *
from Styling import styling

@st.dialog('Debt Details', width='small')
def debt_details(log_df, category_df):
    if not st.session_state.detail_log is None:
        data = st.session_state.detail_log.iloc[0]
        category = category_df.loc[category_df['Category'] == data['Category']]
        flow_text = f"{data['Fund'] + ' → ' + data['Category'] if category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"
        st.markdown(
        f"""<div style="
            border: 1px solid rgba(49, 51, 63, 1);
            border-radius: 10px;
            padding: 12px;
            margin-bottom:5px;
        ">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            ">
                <div style="
                    font-size: 12px;
                    color: gray;
                ">
                    {flow_text}
                </div>
                <div style="
                    font-size: 10px;
                    color: gray;
                ">
                    {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                </div>
            </div>
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="
                    font-size: 18px;
                    font-weight: bold;
                ">
                    Rp {data['Amount']:,}
                </div>
                <div style="
                    font-size: 14px;
                    font-weight: bold;
                    color: #ffffff;
                ">
                    # {data['ID']}
                </div>
            </div>
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="
                    font-size: 10px;
                    color: gray;
                ">
                    {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button('⬅️ Back', width='stretch'):
            st.session_state.detail_log = None
            st.rerun()
    else:
        debt_df = log_df[log_df['Category'].isin(['📋 Debt'])].reset_index()
        for i in range(len(debt_df)):
            data = debt_df.loc[i]
            if data['Ref ID'] != '--':
                pay_data = log_df[log_df['ID'] == data['Ref ID']]
                btn_label_dis = False
                debt_payback = 'Paid'
            else:
                btn_label_dis = True
                debt_payback = 'Unpaid'
            category = category_df.loc[category_df['Category'] == data['Category']]
            flow_text = f"{data['Fund'] + ' → ' + data['Category'] if category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"
            with st.container(horizontal=True):
                with st.container(width='stretch'):
                    st.markdown(
                    f"""<div style="
                        border: 1px solid rgba(49, 51, 63, 1);
                        border-radius: 10px;
                        padding: 12px;
                        margin-bottom:5px;
                    ">
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-bottom: 8px;
                        ">
                            <div style="
                                font-size: 12px;
                                color: gray;
                            ">
                                {flow_text}
                            </div>
                            <div style="
                                font-size: 10px;
                                color: gray;
                            ">
                                {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                            </div>
                        </div>
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        ">
                            <div style="
                                font-size: 18px;
                                font-weight: bold;
                            ">
                                Rp {data['Amount']:,}
                            </div>
                            <div style="
                                font-size: 14px;
                                font-weight: bold;
                                color: {'#28a745' if debt_payback == 'Paid' else '#dc3545'};
                            ">
                                {'✅ Paid' if debt_payback == 'Paid' else '❌ Unpaid'}
                            </div>
                        </div>
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        ">
                            <div style="
                                font-size: 10px;
                                color: gray;
                            ">
                                {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with st.container(width='content'):
                    if st.button('👁️', key=f'debt-btn-info-{i}', disabled=btn_label_dis):
                        st.session_state.detail_log = pay_data
                        st.rerun()
        
        if st.button('❌ Close', width='stretch'):
            st.session_state.debt_dialog = False
            st.rerun()

def debt_display(check, label, amount):
    if check:
        st.session_state[f'{label}_val'] = '******'
        st.session_state[f'show_{label}'] = False
    else:
        st.session_state[f'{label}_val'] = f'Rp. {amount:,}'
        st.session_state[f'show_{label}'] = True

@st.dialog('Lend Details', width='small')
def lend_details(log_df, category_df):
    if not st.session_state.detail_log is None:
        data = st.session_state.detail_log.iloc[0]
        category = category_df.loc[category_df['Category'] == data['Category']]
        flow_text = f"{data['Fund'] + ' → ' + data['Category'] if category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"
        st.markdown(
        f"""<div style="
            border: 1px solid rgba(49, 51, 63, 1);
            border-radius: 10px;
            padding: 12px;
            margin-bottom:5px;
        ">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            ">
                <div style="
                    font-size: 12px;
                    color: gray;
                ">
                    {flow_text}
                </div>
                <div style="
                    font-size: 10px;
                    color: gray;
                ">
                    {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                </div>
            </div>
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="
                    font-size: 18px;
                    font-weight: bold;
                ">
                    Rp {data['Amount']:,}
                </div>
                <div style="
                    font-size: 14px;
                    font-weight: bold;
                    color: #ffffff;
                ">
                    # {data['ID']}
                </div>
            </div>
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div style="
                    font-size: 10px;
                    color: gray;
                ">
                    {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button('⬅️ Back', width='stretch'):
            st.session_state.detail_log = None
            st.rerun()
    else:
        lend_df = log_df[log_df['Category'].isin(['💰 Lending'])].reset_index()
        for i in range(len(lend_df)):
            data = lend_df.loc[i]
            if data['Ref ID'] != '--':
                repay_data = log_df[log_df['ID'] == data['Ref ID']]
                btn_label_dis = False
                lend_repay = 'Repaid'
            else:
                btn_label_dis = True
                lend_repay = 'Unrepaid'
            category = category_df.loc[category_df['Category'] == data['Category']]
            flow_text = f"{data['Fund'] + ' → ' + data['Category'] if category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"
            with st.container(horizontal=True, width='stretch'):
                with st.container(width='stretch'):
                    st.markdown(
                    f"""<div style="
                        border: 1px solid rgba(49, 51, 63, 1);
                        border-radius: 10px;
                        padding: 12px;
                        margin-bottom:5px;
                    ">
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-bottom: 8px;
                        ">
                            <div style="
                                font-size: 12px;
                                color: gray;
                            ">
                                {flow_text}
                            </div>
                            <div style="
                                font-size: 10px;
                                color: gray;
                            ">
                                {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                            </div>
                        </div>
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        ">
                            <div style="
                                font-size: 18px;
                                font-weight: bold;
                            ">
                                Rp {data['Amount']:,}
                            </div>
                            <div style="
                                font-size: 14px;
                                font-weight: bold;
                                color: {'#28a745' if lend_repay == 'Repaid' else '#dc3545'};
                            ">
                                {'✅ Repaid' if lend_repay == 'Repaid' else '❌ Unrepaid'}
                            </div>
                        </div>
                        <div style="
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        ">
                            <div style="
                                font-size: 10px;
                                color: gray;
                            ">
                                {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with st.container(width='content'):
                    if st.button('👁️', key=f'debt-btn-info-{i}', disabled=btn_label_dis):
                        st.session_state.detail_log = repay_data
                        st.rerun()
        
        if st.button('❌ Close', width='stretch'):
            st.session_state.lend_dialog = False
            st.rerun()

def set_date(p):
    st.session_state.current_date = p

def complex_home():
    styling()
    if 'log_df' not in st.session_state:
        st.session_state.log_df = load_data_log()
    if 'funds_df' not in st.session_state:
        st.session_state.funds_df = load_data_fund()
    if 'category_df' not in st.session_state:
        st.session_state.category_df = load_data_category()
    if 'quick_log_df' not in st.session_state:
        st.session_state.quick_log_df = load_data_quick_log()

    if 'log_dialog' not in st.session_state:
        st.session_state.log_dialog = False
    if 'debt_dialog' not in st.session_state:
        st.session_state.debt_dialog = False
    if 'lend_dialog' not in st.session_state:
        st.session_state.lend_dialog = False
        
    if 'detail_log' not in st.session_state:
        st.session_state.detail_log = None

    log_df = st.session_state.log_df
    category_df = st.session_state.category_df
    funds_df = st.session_state.funds_df
    quick_log_df = st.session_state.quick_log_df
    filtered_df = log_df.copy()

    CATEGORY_OPTS = sorted(
        category_df['Category']
        .dropna()
        .unique()
        .tolist()
    )
    
    FUND_OPTS = (
        funds_df['Type']
        .dropna()
        .unique()
        .tolist()
    )

    @st.dialog('Add Log', width='small')
    def add_log():
        if 'selected_ref' not in st.session_state:
            st.session_state.selected_ref = None
        added = False
        cat_opt = CATEGORY_OPTS.copy()
        # timestamp
        log_id = int(datetime.today().timestamp())
        timestamp = date.today().strftime('%d-%m-%Y')

        # fund
        fund = st.selectbox('Fund', options=FUND_OPTS)
        match_fund_data = funds_df[funds_df['Type'] == fund]
        st.write(f'Fund Balance: Rp. {match_fund_data["Balance"].iloc[0]:,}')
        
        # category
        if match_fund_data['Except Category'].iloc[0] !='--':
            excep_list = match_fund_data['Except Category'].iloc[0].split(', ')
            for i in range(len(excep_list)):
                cat_opt.remove(excep_list[i])
        
        category = st.selectbox('Category', options=cat_opt)
        match_category_data = category_df[category_df['Category'] == category].iloc[0]

        if category == '💷 Repayment':
            with st.expander('💰 Lending List', width='stretch'):
                df = log_df[log_df['Category'].isin(['💰 Lending'])]
                for i in df.index:
                    data = df.loc[i]
                    matched_category = category_df.loc[category_df['Category'] == data['Category']]
                    flow_text = f"{data['Fund'] + ' → ' + data['Category'] if matched_category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"
                    with st.container(horizontal=True):
                        with st.container(width='stretch'):
                            st.markdown(
                            f"""<div style="
                                border: 1px solid rgba(49, 51, 63, 1);
                                border-radius: 10px;
                                padding: 12px;
                                margin-bottom:5px;
                            ">
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    margin-bottom: 8px;
                                ">
                                    <div style="
                                        font-size: 12px;
                                        color: gray;
                                    ">
                                        {flow_text}
                                    </div>
                                    <div style="
                                        font-size: 10px;
                                        color: gray;
                                    ">
                                        {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                                    </div>
                                </div>
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                ">
                                    <div style="
                                        font-size: 18px;
                                        font-weight: bold;
                                    ">
                                        Rp {data['Amount']:,}
                                    </div>
                                    <div style="
                                        font-size: 14px;
                                        font-weight: bold;
                                        color: {'#28a745' if matched_category['Type'].iloc[0] == 'Plus' else '#dc3545'};
                                    ">
                                        {'▲ Income' if matched_category['Type'].iloc[0] == 'Plus' else '▼ Expense'}
                                    </div>
                                </div>
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                ">
                                    <div style="
                                        font-size: 10px;
                                        color: gray;
                                    ">
                                        {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                                    </div>
                                </div>
                            </div>""", unsafe_allow_html=True)
                        with st.container(width='content'):
                            if st.session_state.selected_ref == i:
                                btn_type = 'primary'
                            else:
                                btn_type = 'secondary'

                            if st.button('👆', key=f'choose-ref-{i}', type=btn_type):
                                st.session_state.selected_ref = i
                                st.rerun()
                st.space('small')
        elif category == '💸 Payback':
            with st.expander('📋 Debt List:red[*]', width='stretch'):
                df = log_df[(log_df['Category'].isin(['📋 Debt'])) & (log_df['Ref ID'].isin(['--']))]
                for i in df.index:
                    data = df.loc[i]
                    matched_category = category_df.loc[category_df['Category'] == data['Category']]
                    flow_text = f"{data['Fund'] + ' → ' + data['Category'] if matched_category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"
                    with st.container(horizontal=True):
                        with st.container(width='stretch'):
                            st.markdown(
                            f"""<div style="
                                border: 1px solid rgba(49, 51, 63, 1);
                                border-radius: 10px;
                                padding: 12px;
                                margin-bottom:5px;
                            ">
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    margin-bottom: 8px;
                                ">
                                    <div style="
                                        font-size: 12px;
                                        color: gray;
                                    ">
                                        {flow_text}
                                    </div>
                                    <div style="
                                        font-size: 10px;
                                        color: gray;
                                    ">
                                        {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                                    </div>
                                </div>
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                ">
                                    <div style="
                                        font-size: 18px;
                                        font-weight: bold;
                                    ">
                                        Rp {data['Amount']:,}
                                    </div>
                                    <div style="
                                        font-size: 14px;
                                        font-weight: bold;
                                        color: {'#28a745' if matched_category['Type'].iloc[0] == 'Plus' else '#dc3545'};
                                    ">
                                        {'▲ Income' if matched_category['Type'].iloc[0] == 'Plus' else '▼ Expense'}
                                    </div>
                                </div>
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                ">
                                    <div style="
                                        font-size: 10px;
                                        color: gray;
                                    ">
                                        {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                                    </div>
                                </div>
                            </div>""", unsafe_allow_html=True)
                        with st.container(width='content'):
                            if st.session_state.selected_ref == i:
                                btn_type = 'primary'
                            else:
                                btn_type = 'secondary'

                            if st.button('👆', key=f'choose-ref-{i}', type=btn_type):
                                st.session_state.selected_ref = i
                                st.rerun()
                    
                st.space('small')
        else:
            st.session_state.selected_ref = '--'
        
        if st.session_state.selected_ref and st.session_state.selected_ref != '--':
            ref_id = int(log_df.loc[st.session_state.selected_ref, 'ID'])
        else:
            ref_id = '--'
        
        # amount
        if match_category_data['Default Value'] != '--':
            def_val = match_category_data['Default Value']
            dis_amount = False
        elif st.session_state.selected_ref and st.session_state.selected_ref != '--':
            def_val = log_df.loc[st.session_state.selected_ref, 'Amount']
            dis_amount = True
        else:
            def_val = 0
            dis_amount = False

        amount = st.number_input('Amount', width='stretch', value=def_val, disabled=dis_amount)
        st.write(f":gray-background[:green[ℹ️ Inputed : Rp. {amount:,}]]")

        notes = st.text_area('Notes', placeholder='Notes...', width='stretch')
        if not notes:
            notes = '--'

        st.divider()
        st.markdown('### Quick Log')
        with st.container(horizontal=True):
            for i in range(len(quick_log_df)):
                data = quick_log_df.loc[i]
                if st.button(data['Label'], width='content'):
                    fund = data['Fund']
                    category = data['Category']
                    amount = int(data['Amount'])
                    notes = data['Notes']
                    
                    match_category_data = category_df[category_df['Category'] == category].iloc[0]
                    match_fund_data = funds_df[funds_df['Type'] == fund]
                    
                    added = True
            
            if st.button('➕', width='content'):
                notes = notes.split("]", 1)
                label = notes[0].replace('[','').strip()
                if notes[1] != '':
                    note = notes[1].strip()
                else:
                    note = '--'


                new_row = [
                    label,
                    fund,
                    category,
                    amount,
                    note
                ]

                quick_log_df.loc[len(quick_log_df)] = new_row
                st.session_state.quick_log_df = quick_log_df
            
                quick_log_worksheet().append_row(new_row)
                st.toast('✅ Quick Log Added!')
                time.sleep(.5)
                st.rerun()
        st.divider()

        if st.button('💾 Add', width='stretch'):
            added = True

        if added:
            if amount != 0:
                if st.session_state.selected_ref and st.session_state.selected_ref != '--':
                    log_df.at[st.session_state.selected_ref, 'Ref ID'] = str(log_id)
                    row = st.session_state.selected_ref + 2
                    log_worksheet().update(f'G{row}:G{row}', [[log_id]])

                new_row = [
                    log_id,
                    timestamp,
                    fund,
                    category,
                    amount,
                    notes,
                    ref_id
                ]

                log_df.loc[len(log_df)] = new_row
                st.session_state.log_df = log_df

                log_worksheet().append_row(new_row)

                fund_index = match_fund_data.index[0]
                if match_category_data['Type'] == 'Minus':
                    new_balance = match_fund_data['Balance'].iloc[0] - amount
                    if new_balance < 0:
                        st.toast(':red[⚠️ Insufficient Balance!]')
                        st.stop()
                else:
                    new_balance = match_fund_data['Balance'].iloc[0] + amount

                funds_df.at[fund_index, 'Balance'] = new_balance

                label = funds_df.loc[fund_index, 'Type']
                label = '_'.join(label.split(' ',1)[1].lower().split(' '))
                if st.session_state[f'{label}_val'] != '******':
                    st.session_state[f'{label}_val'] = f'Rp. {new_balance:,}'
                
                if category == '💳 BCA' or category == '🪙 Petty Cash':
                    category_fund_index = funds_df[funds_df['Type'] == category].index[0]
                    fund_balance = funds_df.loc[category_fund_index, 'Balance'] + amount
                    funds_df.at[category_fund_index, 'Balance'] = int(fund_balance)
                    row = category_fund_index + 2
                    fund_worksheet().update(f'B{row}:B{row}', [[int(fund_balance)]])

                if category.split(' ',1)[1] == 'Saving':
                    saving_fund = funds_df[funds_df['Type'] == '🏦 Sibuhar']
                    saving_fund_index = saving_fund.index[0]

                    funds_df.at[saving_fund_index, 'Balance'] = saving_fund['Balance'].iloc[0] + amount

                    label = funds_df.loc[saving_fund_index, 'Type']
                    label = '_'.join(label.split(' ',1)[1].lower().split(' '))
                    label_val = saving_fund['Balance'].iloc[0] + amount
                    if st.session_state[f'{label}_val'] != '******':
                        st.session_state[f'{label}_val'] = f'Rp. {label_val:,}'
                    saving_row = saving_fund_index + 2
                    fund_worksheet().update(f'B{saving_row}:B{saving_row}', [[int(saving_fund['Balance'].iloc[0] + amount)]])

                row = fund_index+2
                fund_worksheet().update(f'B{row}:B{row}', [[int(new_balance)]])

                st.toast('✅ Log Added!')
                time.sleep(.5)
                st.session_state.log_dialog = False

                st.rerun()
            else:
                st.toast(':red[⚠️ Amount must bigger than 0!]')
        
        if st.button('❌ Cancel', width='stretch'):
            st.session_state.log_dialog = False
            st.rerun()

    with st.sidebar:
        cat_opt = ['🗒️ All'] + CATEGORY_OPTS.copy()
        st.radio('Page', options=['Home', 'Settings'], key='home_page', horizontal=True)
        category_filter = st.selectbox('Category', width='stretch', options=cat_opt)
        date_filter = st.selectbox('Date Filter', options=['📅 Day', '📅 Month/Year', '📅 Year'])
        date_filter = date_filter.split(' ',1)[1]

        st.divider()

        shown = ['💳 BCA', '🪙 Petty Cash', '🏦 Sibuhar']
        index = 0

        for i in shown:
            label = '_'.join(i.split(' ',1)[1].lower().split(' '))
            session_label_show = f'show_{label}'
            session_label_amount = f'{label}_val'

            if session_label_show not in st.session_state:
                st.session_state[session_label_show] = False
            if session_label_amount not in st.session_state:
                st.session_state[session_label_amount] = '******'

            with st.container(key=f'navbar-fund-info-{i}', horizontal=True):
                with st.container(horizontal=True, width='stretch'):
                    with st.container(width='stretch'):
                        st.markdown(
                            f"""<div style="font-size: 10px; color: gray; text-align:center;">
                                    {i}
                                </div>
                                <div style="font-size: 18px; font-weight: bold; text-align:center;">
                                    {st.session_state[session_label_amount]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with st.container(key=f'show-eye-{index}', width='content'):
                        st.button("👁️", on_click=debt_display, args=(st.session_state[session_label_show], label, funds_df.loc[funds_df['Type'] == i, 'Balance'].iloc[0]), key=f'show-button-{index}')
                index+=1

        st.divider()
        st.markdown("""
            <style>
                [class*="st-key-navbar-fund-info-"]{
                    text-align: center !important;
                    border: 1px solid rgba(250, 250, 250, 0.2);
                    border-radius: 10px;
                    padding: 12px;
                }
            </style>
        """, unsafe_allow_html=True)
        debt_df = log_df[log_df['Category'].isin(['📋 Debt', '💸 Payback'])].reset_index()
        debt = 0
        pay = 0
        for i in range(len(debt_df)):
            data = debt_df.loc[i]

            if data['Category'] == '📋 Debt':
                debt +=data['Amount']
            else:
                pay += data['Amount']
        
        debt_left = debt - pay

        lend_df = log_df[log_df['Category'].isin(['💰 Lending', '💷 Repayment'])].reset_index()
        lend = 0
        repay = 0
        for i in range(len(lend_df)):
            data = lend_df.loc[i]

            if data['Category'] == '💰 Lending':
                lend +=data['Amount']
            else:
                repay += data['Amount']

        lend_left = lend - repay

        if 'show_debt' not in st.session_state:
            st.session_state.show_debt = False
        if 'debt_val' not in st.session_state:
            st.session_state.debt_val = '******'
        if 'show_lend' not in st.session_state:
            st.session_state.show_lend = False
        if 'lend_val' not in st.session_state:
            st.session_state.lend_val = '******'

        with st.container(key=f'navbar-fund-info-debt'):
            with st.container(horizontal=True, width='stretch'):
                with st.container(width='stretch'):
                    st.markdown(
                        f"""<div style="font-size: 10px; color: gray; text-align: center;">
                                💸 Debt
                            </div>
                            <div style="font-size: 18px; font-weight: bold; text-align: center;">
                                {st.session_state.debt_val}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with st.container(key='debt-eye', width='content'):
                    st.button("👁️", on_click=debt_display, args=(st.session_state.show_debt, 'debt', debt_left), key='debt-eye-btn')
                with st.container(key='debt-detail', width='content'):
                    if st.button("🗒️", key='debt-detail-btn'):
                        st.session_state.debt_dialog = True

        with st.container(key='navbar-fund-info-lend'):
            with st.container(horizontal=True, width='stretch'):
                with st.container(width='stretch'):
                    st.markdown(
                        f"""<div style="font-size: 10px; color: gray; text-align: center;">
                                💰 Lending
                            </div>
                            <div style="font-size: 18px; font-weight: bold; text-align: center;">
                                {st.session_state.lend_val}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with st.container(key='lend-eye', width='content'):
                    st.button("👁️", on_click=debt_display, args=(st.session_state.show_lend, 'lend', lend_left), key='lend-eye-btn')
                with st.container(key='lend-detail', width='content'):
                    if st.button("🗒️", key='lend-detail-btn'):
                        st.session_state.lend_dialog = True
                        st.rerun()
            
    film_navbar = st.container(key='film-navbar', width='stretch', horizontal=True, horizontal_alignment='right')
    
    with film_navbar:
        if st.session_state.home_page == 'Settings':
            if st.button('➕ Category'):
                @st.dialog('Add Category', width='small')
                def add_category():
                    icon_list = category_df['Category'].str.split(' ',n=1).str[0].to_list()
                    category_list = category_df['Category'].str.split(' ',n=1).str[1].to_list()

                    category = st.text_input('Category:red[*]', placeholder='Type Category...', width="stretch")
                    icon = st.text_input('Icon:red[*]', placeholder='Input Icon...', width="stretch")
                    default_val = st.number_input('Default Value:red[*]', min_value=0, width='stretch')
                    st.write(f":gray-background[:green[ℹ️ Inputed : Rp. {default_val:,}]]")

                    category_type = st.radio('Type:red[*]', options=['Plus', 'Minus'], width='stretch', horizontal=True)

                    if st.button('➕ Add', width='stretch'):
                        if category and icon:
                            if icon.strip() not in icon_list:
                                if category.strip() not in category_list:
                                    if default_val == 0:
                                        default_val = '--'

                                    new_row = [
                                        icon + ' ' + category,
                                        str(default_val),
                                        category_type
                                    ]

                                    category_worksheet().append_row(new_row)
                                    category_df.loc[len(category_df)] = new_row
                                    st.session_state.category_df = category_df

                                    st.rerun()
                                else:
                                    st.warning(f'Category {category.strip()} already exist in database!')
                            else:
                                st.warning(f'Icon {icon.strip()} already exist in database!')
                        else:
                            st.warning(f'Fill mandatory fields first! (:red[*])')
                    
                    if st.button('❌ Close', width='stretch', type='primary'):
                        st.rerun()
                add_category()
            
            if st.button('➕ Funds'):
                @st.dialog('Add Funds', width='small')
                def add_funds():
                    funds_list = funds_df['Type'].str.split(' ',n=1).str[1].to_list()

                    funds = st.text_input('funds:red[*]', placeholder='Type funds...', width="stretch")
                    icon = st.text_input('Icon:red[*]', placeholder='Input Icon...', width="stretch")
                    default_val = st.number_input('Default Value:red[*]', min_value=0, width='stretch')
                    st.write(f":gray-background[:green[ℹ️ Inputed : Rp. {default_val:,}]]")


                    if st.button('➕ Add', width='stretch'):
                        if funds and icon:
                            if funds.strip() not in funds_list:
                                new_row = [
                                    icon + ' ' + funds,
                                    default_val
                                ]

                                funds_df.loc[len(funds_df)] = new_row
                                st.session_state.funds_df = funds_df

                                fund_worksheet().append_row([icon + ' ' + funds, default_val])
                                st.rerun()
                            else:
                                st.warning(f'funds {funds.strip()} already exist in database!')
                        else:
                            st.warning(f'Fill mandatory fields first! (:red[*])')
                    
                    if st.button('❌ Close', width='stretch', type='primary'):
                        st.rerun()
                add_funds()
        else:
            # if date_filter == 'Day':
            #     if st.button('📅 Go To'):
            #         st.write('hello')

            st.button('📅 Today', on_click=set_date, args=(date.today(),))
            if st.button('➕ Log'):
                st.session_state.log_dialog = True
                st.rerun()
    
    if st.session_state.log_dialog:
        add_log()

    if st.session_state.debt_dialog:
        debt_details(log_df, category_df)
    
    if st.session_state.lend_dialog:
        lend_details(log_df, category_df)

    film_navbar.float("top: 50px;z-index: 999990;")

    if st.session_state.home_page == 'Home':
        if 'edit_log' not in st.session_state:
            st.session_state.edit_log = None
        if 'current_date' not in st.session_state:
            st.session_state.current_date = date.today()

        @st.dialog('Log Detail', width='small')
        def edit_log():
            index = st.session_state.edit_log
            log = log_df.loc[index]
            matched_fund = funds_df[funds_df['Type'] == log['Fund']] 
            matched_fund_index = matched_fund.index[0]
            matched_category = category_df[category_df['Category'] == log['Category']]

            if log['Notes'] == '--':
                note_text = ''
            else:
                note_text = log['Notes']

            fund_index = FUND_OPTS.index(log['Fund']) if log['Fund'] in FUND_OPTS else 0
            category_index = CATEGORY_OPTS.index(log['Category']) if log['Category'] in CATEGORY_OPTS else 0

            with st.container(horizontal_alignment='distribute', horizontal=True): 
                st.write(f'ID -- #{log["ID"]}')
                st.write(datetime.strptime(log["Timestamp"], "%d-%m-%Y").strftime("%d %B %Y"))
            st.divider()

            fund = st.selectbox('Fund', options=FUND_OPTS, index=fund_index)
            selected_fund = funds_df[funds_df['Type'] == fund]
            selected_fund_index = selected_fund.index[0]
                
            category = st.selectbox('Category', options=CATEGORY_OPTS, index=category_index)
            selected_category = category_df[category_df['Category'] == category]

            amount = st.number_input('Amount', value=log['Amount'])
            note = st.text_area('Notes', value=note_text, placeholder='Notes...')
            
            if not note:
                note = '--'

            st.divider()

            if st.button('💾 Save', width='stretch'):
                if fund != log['Fund']:
                    if matched_category['Type'].iloc[0] == 'Plus':
                        reset_balance = matched_fund['Balance'].iloc[0] - log['Amount'] 
                    else:
                        reset_balance = matched_fund['Balance'].iloc[0] + log['Amount'] 

                    funds_df.at[matched_fund_index, 'Balance'] = reset_balance

                    label = funds_df.loc[matched_fund_index, 'Type']
                    label = '_'.join(label.split(' ',1)[1].lower().split(' '))
                    if st.session_state[f'{label}_val'] != '******':
                        st.session_state[f'{label}_val'] = f'Rp. {reset_balance:,}'

                    if selected_category['Type'].iloc[0] == 'Plus':
                        new_balance = selected_fund['Balance'].iloc[0] + amount
                    else:
                        new_balance = selected_fund['Balance'].iloc[0] - amount
                    funds_df.at[selected_fund_index, 'Balance'] = new_balance

                    label = funds_df.loc[selected_fund_index, 'Type']
                    label = '_'.join(label.split(' ',1)[1].lower().split(' '))
                    if st.session_state[f'{label}_val'] != '******':
                        st.session_state[f'{label}_val'] = f'Rp. {new_balance:,}'

                    reset_row = matched_fund_index + 2
                    new_row = selected_fund_index + 2

                    batch_data = [
                        {
                            "range": f"B{reset_row}:B{reset_row}",
                            "values": [[int(reset_balance)]],
                        },
                        {
                            "range": f"B{new_row}:B{new_row}",
                            "values": [[int(new_balance)]],
                        }
                    ]

                    fund_worksheet().batch_update(batch_data)

                    
                
                if fund == log['Fund'] and amount != log['Amount']:
                    if matched_category['Type'].iloc[0] == 'Plus':
                        new_balance = matched_fund['Balance'].iloc[0] - log['Amount']
                        if selected_category['Type'].iloc[0] == 'Plus':
                            new_balance += amount
                        else:
                            new_balance -= amount
                    else:
                        new_balance = matched_fund['Balance'].iloc[0] + log['Amount']
                        if selected_category['Type'].iloc[0] == 'Plus':
                            new_balance += amount
                        else:
                            new_balance -= amount
                        
                    funds_df.at[matched_fund_index, 'Balance'] = new_balance

                    label = funds_df.loc[matched_fund_index, 'Type']
                    label = '_'.join(label.split(' ',1)[1].lower().split(' '))
                    if st.session_state[f'{label}_val'] != '******':
                        st.session_state[f'{label}_val'] = f'Rp. {new_balance:,}'

                    new_row = matched_fund_index + 2
                    fund_worksheet().update(f'B{new_row}:B{new_row}', [[int(new_balance)]])

                st.session_state.funds_df = funds_df
                
                updated_row = [
                    log['Timestamp'],
                    fund,
                    category,
                    amount,
                    note
                ]

                log_df.loc[index] = updated_row

                row = index + 2
                log_worksheet().update(f'A{row}:E{row}', [updated_row])
                st.session_state.log_df = log_df
                st.session_state.edit_log = None
                st.rerun()
            
            if st.button('🗑️ Delete', width='stretch'):
                if log['Ref ID'] != '--':
                    ref_id = log['Ref ID']
                    matched_ref_index = log_df[log_df['ID'] == ref_id].index[0]
                    log_df.at[matched_ref_index, 'Ref ID'] = '--'
                    row = matched_ref_index + 2
                    log_worksheet().update(f'G{row}:G{row}', [['--']])
                log_worksheet().delete_rows(index+2)
                st.session_state.log_df = log_df.drop(index)

                if matched_category['Type'].iloc[0] == 'Plus':
                    reset_balance = matched_fund['Balance'].iloc[0] - log['Amount']
                else:
                    reset_balance = matched_fund['Balance'].iloc[0] + log['Amount']

                funds_df.at[matched_fund_index, 'Balance'] = reset_balance

                label = funds_df.loc[matched_fund_index, 'Type']
                label = '_'.join(label.split(' ',1)[1].lower().split(' '))
                if st.session_state[f'{label}_val'] != '******':
                    st.session_state[f'{label}_val'] = f'Rp. {reset_balance:,}'

                row = matched_fund_index + 2
                st.session_state.funds_df = funds_df
                fund_worksheet().update(f'B{row}:B{row}', [[int(reset_balance)]])
                st.session_state.edit_log = None
                st.toast(f'✅ Log ID {index} deleted!')
                time.sleep(.5)
                st.rerun()

            if st.button('❌ Close', width='stretch'):
                st.session_state.edit_log = None
                st.rerun()

        today = st.session_state.current_date

        if category_filter != '🗒️ All':
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]
        
        filtered_df['filtered_date'] = pd.to_datetime(
            filtered_df['Timestamp'],
            format='%d-%m-%Y',
            errors='coerce'
        )

        st.markdown("<h1 style='text-align: center;'>Cash Flow</h1>", unsafe_allow_html=True)
        if date_filter == 'Month/Year':
            st.markdown(f"<h2 style='text-align: center;'>{today.strftime('%B %Y')}</h2>", unsafe_allow_html=True)
            filtered_df = filtered_df[filtered_df['filtered_date'].dt.month == st.session_state.current_date.month]
        elif date_filter == 'Day':
            st.markdown(f"<h2 style='text-align: center;'>{today.strftime('%d %B %Y')}</h2>", unsafe_allow_html=True)
            filtered_df = filtered_df[filtered_df['filtered_date'].dt.date == st.session_state.current_date]
        elif date_filter == 'Year':
            st.markdown(f"<h2 style='text-align: center;'>{today.strftime('%Y')}</h2>", unsafe_allow_html=True)
            filtered_df = filtered_df[filtered_df['filtered_date'].dt.year == st.session_state.current_date.year]


        with st.container(horizontal=True):
            if date_filter == 'Month/Year':
                date_next = st.session_state.current_date + relativedelta(months=1)
                date_prev = st.session_state.current_date - relativedelta(months=1)
            if date_filter == 'Day':
                date_next = st.session_state.current_date + relativedelta(days=1)
                date_prev = st.session_state.current_date - relativedelta(days=1)
            if date_filter == 'Year':
                date_next = st.session_state.current_date + relativedelta(years=1)
                date_prev = st.session_state.current_date - relativedelta(years=1)
            st.button('⬅️', width='stretch', on_click=set_date, args=(date_prev,))
            st.button('➡️', width='stretch', on_click=set_date, args=(date_next,))
        
        st.divider()
        if filtered_df.empty:
            st.warning('⚠️ No Data!')
        else:
            for i in filtered_df.index:
                data = filtered_df.loc[i]
                if data['Category'] == '💳 BCA' or data['Category'] == '🪙 Petty Cash':
                    btn_dis = True
                else:
                    btn_dis = False
                category = category_df.loc[category_df['Category'] == data['Category']]
                
                flow_text = f"{data['Fund'] + ' → ' + data['Category'] if category['Type'].iloc[0] == 'Minus' else data['Category'] + ' → ' + data['Fund']}"

                if data['Category'] in ['💳 BCA', '🪙 Petty Cash']:
                    log_background_color = '#d1ecf1'   
                    log_info_color = '#0c5460'         
                    log_nominal_color = '#084298'      
                    log_status_color = '#0d6efd'       
                    log_status_text = '⇄ Transfer'       
                elif category['Type'].iloc[0] == 'Plus':
                    log_background_color = '#d4edda'
                    log_info_color = '#155724'
                    log_nominal_color = '#0f5132'
                    log_status_color = '#28a745'
                    log_status_text = '▲ Income'
                else:
                    log_background_color = '#f8d7da'
                    log_info_color = '#721c24'
                    log_nominal_color = '#58151c'
                    log_status_color = '#dc3545'
                    log_status_text = '▼ Expense'


                with st.container(horizontal=True, horizontal_alignment='distribute'):
                    with st.container(width='stretch'):
                        st.markdown(
                            f"""<div style="
                                border: 1px solid {log_status_color};
                                border-radius: 10px;
                                padding: 12px;
                                margin-bottom:5px;
                                background-color: {log_background_color};
                            ">
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                    margin-bottom: 8px;
                                ">
                                    <div style="
                                        font-size: 12px;
                                        color: {log_info_color};
                                    ">
                                        {flow_text}
                                    </div>
                                    <div style="
                                        font-size: 10px;
                                        color: {log_info_color};
                                    ">
                                        {datetime.strptime(data['Timestamp'], '%d-%m-%Y').strftime('%d %B %Y')}
                                    </div>
                                </div>
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                ">
                                    <div style="
                                        font-size: 18px;
                                        font-weight: bold;
                                        color: {log_nominal_color};
                                    ">
                                        Rp {data['Amount']:,}
                                    </div>
                                    <div style="
                                        font-size: 14px;
                                        font-weight: bold;
                                        color: {log_status_color};
                                    ">
                                        {log_status_text}
                                    </div>
                                </div>
                                <div style="
                                    display: flex;
                                    justify-content: space-between;
                                    align-items: center;
                                ">
                                    <div style="
                                        font-size: 10px;
                                        color: {log_info_color};
                                    ">
                                        {'Notes : ' + data['Notes'] if data['Notes'] != '--' else 'Notes : -'}
                                    </div>
                                </div>
                            </div>""", unsafe_allow_html=True)
                    if st.button('✏️', key=f'edit_log_{i}', width='content', disabled=btn_dis, type='tertiary'):
                        st.session_state.edit_log = i
        st.divider()

        if not st.session_state.edit_log is None:
            edit_log()
    
    else:
        if 'edit_amount' not in st.session_state:
            st.session_state.edit_amount = None
        if 'edit_category' not in st.session_state:
            st.session_state.edit_category = None
        if 'edit_quick_log' not in st.session_state:
            st.session_state.edit_quick_log = None
        
        st.markdown("<h1 style='text-align: center;'>Setting</h1>", unsafe_allow_html=True)
        st.divider()
        st.subheader('Funds')
        with st.expander('Expand', width='stretch'):
            for i in range(len(funds_df)):
                data = funds_df.iloc[i]
                with st.container(horizontal=True, horizontal_alignment='distribute', width='stretch'):
                    with st.container(width='content'):
                        st.markdown(
                            f"""
                            <div style="height:38px; display:flex; align-items:center;">
                                <span>
                                    {data['Type']} :
                                </span>
                                <span style="color:{'red' if data['Balance'] < 0 else '#5CE488'}; margin-left:5px;">
                                    Rp. {data['Balance']:,}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with st.container(horizontal=True, width='content'):
                        if st.button('✏️', type='tertiary', key=f'edit_fund_{i}'):
                            st.session_state.edit_amount = i
                            st.rerun()
                            
                        if st.button('🗑️', type='tertiary', key=f'delete_fund_{i}'):
                            st.session_state.funds_df = funds_df.drop(i)
                            row = i+2
                            fund_worksheet().delete_rows(row,row)
                            st.rerun()
                
                if st.session_state.edit_amount == i:
                    new_amount = st.number_input(f'{data["Type"]} Balance', min_value=0, value=data['Balance'])
                    st.write(f":gray-background[:green[ℹ️ Inputed : Rp. {new_amount:,}]]")

                    if data['Except Category'] != '--':
                        default_except = data['Except Category'].split(', ')
                    else:
                        default_except = []


                    sel_except = st.multiselect('Exception', options=CATEGORY_OPTS, default=default_except)
                    if sel_except:
                        new_except = ', '.join(sel_except)
                    else:
                        new_except = '--'

                    with st.container(horizontal=True, vertical_alignment='bottom', width='stretch'):
                        if st.button('💾', key=f'save_fund_{i}', width='stretch'):
                            funds_df.at[i, 'Balance'] = new_amount
                            funds_df.at[i, 'Except Category'] = new_except

                            new_row = [
                                new_amount,
                                new_except
                            ]

                            st.session_state.funds_df = funds_df

                            row = i+2
                            fund_worksheet().update(f'B{row}:C{row}', [new_row])

                            st.session_state.edit_amount = None
                            st.toast('✅ Edit saved!')
                            time.sleep(.5)
                            st.rerun()
                        if st.button('❌', key=f'cancel_fund_{i}', width='stretch'):
                            st.session_state.edit_amount = None
                            st.rerun()
                    st.divider()
            
        st.subheader('Category')
        with st.expander('Expand', width='stretch'):
            for i in range(len(category_df)):
                data = category_df.iloc[i]
                with st.container(horizontal=True, horizontal_alignment='distribute', width='stretch'):
                    with st.container(width='content'):
                        st.markdown(
                            f"""
                            <div style="height:38px; display:flex; align-items:center;">
                                <span>
                                    {data['Category']}
                                </span>
                                <span style="color: white; margin-left:5px;">
                                    ({'Rp. ' + str(data['Default Value']) if data['Default Value'] != '--' else '--'})
                                </span>
                                <span style="color: {'red' if data['Type'] == 'Minus' else '#5CE488'}; margin-left:5px;">
                                    ({data['Type']})
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with st.container(horizontal=True, width='content'):
                        if st.button('✏️', type='tertiary', key=f'edit_category_{i}'):
                            st.session_state.edit_category = i
                            st.rerun()
                            
                        if st.button('🗑️', type='tertiary', key=f'delete_category_{i}'):
                            st.session_state.category_df = category_df.drop(i)
                            row = i+2
                            category_worksheet().delete_rows(row,row)
                            st.rerun()
                
                if st.session_state.edit_category == i:
                    with st.container():
                        with st.container(horizontal=True, vertical_alignment='bottom'):
                            def_val = data['Default Value'] if data['Default Value'] != '--' else 0
                            new_category = st.number_input(f'{data["Category"]} Default Balance', min_value=0, value=def_val)

                            if st.button('💾', key=f'save_category_{i}'):
                                category_df.at[i, 'Balance'] = new_category
                                st.session_state.category_df = category_df
                                row = i+2
                                category_worksheet().update(f'B{row}:B{row}', [[new_category]])
                                st.session_state.edit_category = None

                                st.rerun()
                            if st.button('❌', key=f'cancel_category_{i}'):
                                st.session_state.edit_category = None
                                st.rerun()
                        st.write(f":gray-background[:green[ℹ️ Inputed : Rp. {new_category:,}]]")
                        st.divider()

        st.subheader('Quick Log')
        with st.expander('Expand', width='stretch'):
            for i in range(len(quick_log_df)):
                data = quick_log_df.iloc[i]
                with st.container(horizontal=True, horizontal_alignment='distribute', width='stretch'):
                    with st.container(width='content'):
                        st.markdown(
                            f"""
                            <div style="height:38px; display:flex; align-items:center;">
                                <span>
                                    {data['Label']}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with st.container(horizontal=True, width='content'):
                        if st.button('✏️', type='tertiary', key=f'edit_quick_log_{i}'):
                            st.session_state.edit_quick_log = i
                            
                        if st.button('🗑️', type='tertiary', key=f'delete_quick_log{i}'):
                            st.session_state.quick_log_df = quick_log_df.drop(i)
                            row = i+2
                            quick_log_worksheet().delete_rows(row,row)
                            st.rerun()
                
                if st.session_state.edit_quick_log == i:
                    cat_opt = CATEGORY_OPTS.copy()

                    fund_index = FUND_OPTS.index(data['Fund']) if data['Fund'] in FUND_OPTS else 0
                    edit_label = st.text_input('Label', value=data['Label'], placeholder='Label...', width='stretch')

                    edit_fund = st.selectbox('Fund', options=FUND_OPTS, index=fund_index, width='stretch')
                    match_fund_data = funds_df[funds_df['Type'] == edit_fund]
                    
                    # category
                    if match_fund_data['Except Category'].iloc[0] !='--':
                        excep_list = match_fund_data['Except Category'].iloc[0].split(', ')
                        for i in range(len(excep_list)):
                            cat_opt.remove(excep_list[i])
                    
                    category_index = cat_opt.index(data['Category']) if data['Category'] in cat_opt else 0
                    edit_category = st.selectbox('Category', options=cat_opt, index=category_index)
                    edit_ammount = st.number_input('Amount', value=data['Amount'], min_value=0)
                    st.write(f":gray-background[:green[ℹ️ Inputed : Rp. {edit_ammount:,}]]")

                    if data['Notes'] == '--':
                        notes = ''
                    else:
                        notes = data['Notes']

                    edit_notes = st.text_area('Notes', width='stretch', placeholder='Notes...', value=notes)

                    if not edit_notes:
                        edit_notes = '--'

                    with st.container(horizontal=True, vertical_alignment='bottom'):
                        if st.button('❌', key=f'cancel_quick_log_{i}', width='stretch'):
                            st.session_state.edit_quick_log = None
                            st.rerun()
                        if st.button('💾', key=f'save_quick_log_{i}', width='stretch'):
                            edit_row = [
                                edit_label,
                                edit_fund,
                                edit_category,
                                edit_ammount,
                                edit_notes
                            ]

                            quick_log_df.at[i, 'Label'] = edit_label
                            quick_log_df.at[i, 'Fund'] = edit_fund
                            quick_log_df.at[i, 'Category'] = edit_category
                            quick_log_df.at[i, 'Amount'] = edit_ammount
                            quick_log_df.at[i, 'Notes'] = edit_notes

                            st.session_state.quick_log_df = quick_log_df
                            row = i+2
                            quick_log_worksheet().update(f'A{row}:E{row}', [edit_row])
                            st.session_state.edit_quick_log = None
                            st.toast(f'✅ Quick Log {edit_label} updated!')
                            time.sleep(.5)
                            st.rerun()
                    st.divider()

        st.divider()
