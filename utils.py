import pandas as pd
import streamlit as st
import hashlib
import os
from dotenv import load_dotenv

def pivot_report_status(df):
    temp = pd.pivot_table(df, index='List_of_Sites_SHS_Portfolio',
                          columns='Report_Status', aggfunc='count')[['WeekPeriod']].reset_index()
    temp.columns = ['ProgramName', 'Missing', 'Completed']
    return temp

def pivot_weeks_by_facility(df):
    temp = pd.pivot_table(df, index=['Facility_Type','List_of_Sites_SHS_Portfolio','PA'],
                          aggfunc={'WeekPeriod':'count'}).reset_index()
    temp.columns = ['Facility_Type','ProgramName','PA','No_of_Weeks']
    return temp

def pivot_late_submissions(df):
    temp = pd.pivot_table(df, index='List_of_Sites_SHS_Portfolio',
                          columns='Late_Submission_FLG', aggfunc='count')[['WeekPeriod']].reset_index()
    if len(df['Late_Submission_FLG'].unique()) == 2: 
        temp.columns = ['ProgramName','N','Delayed_Entry']
    elif len(df['Late_Submission_FLG'].unique()) == 1 & df['Late_Submission_FLG'].unique() == ['N']: 
        temp.columns = ['ProgramName', 'N']
    elif len(df['Late_Submission_FLG'].unique()) == 1 & df['Late_Submission_FLG'].unique() == ['Y']:
        temp.columns = ['ProgramName', 'Y']
        temp.rename(columns={'Y':'Delayed_Entry'})
    return temp

'''
def build_reporting_tables(df):

    temp1 = pivot_report_status(df)
    temp2 = pivot_weeks_by_facility(df)
    temp3 = pivot_late_submissions(df)

    merged = temp1.merge(temp2, how='left').merge(temp3[['ProgramName','Delayed_Entry']], how='left').fillna(0)
    merged = merged[['Facility_Type','ProgramName','PA','Completed','No_of_Weeks','Delayed_Entry']]
    merged['%Reported'] = round(merged['Completed']/merged['No_of_Weeks']*100,1)
    merged = merged.sort_values(by=['Facility_Type','%Reported'], ascending=False)

    return {ftype: merged[merged['Facility_Type']==ftype] for ftype in merged['Facility_Type'].unique()}
'''

def build_reporting_tables(df):

    if df.empty:
        return {}

    temp1 = pivot_report_status(df)
    temp2 = pivot_weeks_by_facility(df)
    temp3 = pivot_late_submissions(df)

    merged = (
        temp1
        .merge(temp2, how='left')
        .merge(temp3[['ProgramName','Delayed_Entry']], how='left')
        .fillna(0)
    )

    merged = merged[['Facility_Type','ProgramName','PA','Completed','No_of_Weeks','Delayed_Entry']]

    merged['%Reported'] = (
        merged['Completed'] / merged['No_of_Weeks'].replace(0,1) * 100
    ).round(1)

    merged = merged.sort_values(
        by=['Facility_Type','%Reported'],
        ascending=False
    )

    return {
        ftype: merged[merged['Facility_Type']==ftype]
        for ftype in merged['Facility_Type'].unique()
    }

def small_table_view(df):
    row_height = 35
    if len(df) <= 20:  # small table → show all rows
        st.table(df)
    else:
        table_height = min(600, row_height * len(df))
        st.dataframe(df, height=table_height)


def get_table_height(df):

    row_height = 35  # pixels per row, adjust if you want
    max_height = 900
    table_height = min(max_height, row_height * len(df))  # max height to avoid huge tables

    return table_height

# Load .env from project root
# load_dotenv('venv\\.env')
# USERNAME = os.getenv("LOGIN_ID")
# PASSWORD_HASH = os.getenv("PASSWORD_HASH")  

import hashlib
USERNAME =st.secrets["USERNAME"]
PASSWORD_HASH = st.secrets["PASSWORD_HASH"]

''' 
def check_login():
   
    st.sidebar.title("🔒 Login")

    # Sidebar input fields
    username_input = st.sidebar.text_input("Username")
    password_input = st.sidebar.text_input("Password", type="password")

    if username_input and password_input:
        hashed_input = hashlib.sha256(password_input.encode()).hexdigest()
        if username_input == USERNAME and hashed_input == PASSWORD_HASH:
            st.sidebar.success("✅ Access granted")
            return True
        else:
            st.sidebar.error("❌ Access denied")
            st.stop()
    else:
        st.sidebar.info("Please enter your credentials")
        st.stop()
    '''

'''
    # Create a login form widget
    with st.form("login_form"):
        st.write("🔒 Please log in to access the dashboard")
        username_input = st.text_input("Username").strip()
        password_input = st.text_input("Password", type="password").strip()
        submitted = st.form_submit_button("Login")

        if submitted:
            hashed_input = hashlib.sha256(password_input.encode()).hexdigest()
            if username_input == USERNAME and hashed_input == PASSWORD_HASH:
                st.success("✅ Access granted")
                return True
            else:
                st.error("❌ Access denied")
                st.stop()
        else:
            st.info("Enter your credentials and click Login")
            st.stop()

'''

def login_form():
    with st.form("login_form"):
        st.write("🔒 Please log in to access the dashboard")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:            
            hashed_input = hashlib.sha256(password_input.encode()).hexdigest()
            if username_input == USERNAME and hashed_input == PASSWORD_HASH:
                st.session_state.logged_in = True
                st.success("✅ Access granted")
            else:
                st.error("❌ Access denied")
