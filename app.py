import streamlit as st
import pandas as pd
## from sql_load import get_data, get_csv
from utils import login_form
## from dotenv import load_dotenv
import os
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() =="true"

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login form only if not logged in
if not st.session_state.logged_in:
    login_form()
    st.stop()  # Stop the rest of the app until login succeeds

st.set_page_config(
    page_title = "Reporting Compliance Dashboard", 
    layout= "wide"
)

## with st.expander("About this dashboard"):
##    st.write("This demo uses dummy data for viewing purposes.")

st.title("Report Compliance Demo Dashboard")
## REal Title: st.title("SHS Projected Exits Dashboard")
st.caption("Prototpe Internal Monitoring Tool - Created on March 9, 2026")
st.info("Demo version using synthetic data for UI & viewing purposes.")
st.write("")
st.write("Please select report type to view.")

'''
# Load data directly from SQL
try: 
    from pathlib import Path
    from datetime import datetime, timedelta
    file_path = Path("data\\compliance.csv")
    last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
    last_modified = pd.to_datetime(str(last_modified)[:10])

    today = datetime.today()
    days_since_modified = today - last_modified

    if days_since_modified > timedelta(days=7) :
        st.warning("Data Needs Update - loading from SQL")
        compliance, pmo_data, reentry_data = get_data()
        get_csv()
        ## st.write(compliance.head())
        ## st.write(pmo_data.head())
        ## st.write(reentry_data)

    else: 
        compliance, pmo_data, reentry_data = get_csv()
        ## st.write(compliance.head())
        ## st.write(pmo_data.head())
        ## st.write(reentry_data)
        
except Exception:
    st.warning("Data Needs Update - loading from SQL") 
    compliance, pmo_data, reentry_data = get_csv()

    try: 
        compliance, pmo_data, reentry_data = get_data()
        get_csv()
        ## st.write(compliance.head())
        ## st.write(pmo_data.head())
        ## st.write(reentry_data)

    except Exception as e:
        st.error("SQL load failed")
        st.write(e)
'''
## Replace data to demo data

if DEMO_MODE: 
    compliance = pd.read_csv("data_dummy\\compliance_dummy.csv")
    data = pd.read_csv("data_dummy\\compliance_dummy.csv")
else: 
    pass

st.sidebar.header("Filters & Views")
st.sidebar.write('Select date range for report view.')

# Date range filter
min_date = pd.to_datetime(compliance['StartOfWeek']).min()
max_date = pd.to_datetime(compliance['EndOfWeek']).max()

date_range = st.sidebar.date_input(
    "Select Date Range", 
    [min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = compliance[
        (pd.to_datetime(compliance['StartOfWeek']) >=pd.to_datetime(start_date)) &
        (pd.to_datetime(compliance['EndOfWeek']) <= pd.to_datetime(end_date))
    ]

    from utils import pivot_late_submissions, pivot_report_status, pivot_weeks_by_facility, build_reporting_tables, get_table_height
    ## data = filtered_df.copy()

    st.sidebar.header("Filters")

    type_list = sorted(data['Facility_Type'].dropna().unique())
    selected_type = st.sidebar.selectbox(
        "Program Type", 
        options=['All'] + type_list
    )

    df_select = data
    if selected_type != 'All':
        df_select = df_select[df_select['Facility_Type']== selected_type]
    
    pa_list = sorted(data['PA'].dropna().unique())
    selected_pa = st.sidebar.selectbox(
        "Filter by PA",
        options=['All'] + pa_list
    )

    program_list = sorted(df_select['List_of_Sites_SHS_Portfolio'].dropna().unique())

    selected_name = st.sidebar.selectbox(
        "Program Name", 
        options=['All'] + program_list
    )

    if selected_type != 'All':
        data = data[
            data['Facility_Type']==selected_type
        ]
    if selected_name != 'All':
            data = data[
                data['List_of_Sites_SHS_Portfolio'] == selected_name
            ]
    if selected_pa != 'All':
            data = data[
                data['PA'] == selected_pa
            ]
    if data.empty: 
            st.write("No data returned for selected filters. Try adjusting the date range or site.")
            st.stop()

    facility_dict = build_reporting_tables(data)

    if not facility_dict:
        st.warning("No data returned for selected filters. Try adjusting the date range or site.")
        st.stop()
    
    
    # Map friendly tab names to facility types

    if DEMO_MODE: 
        tab_map = {"Fruit Pie":"Fruit Pie", "Candy Canes":"Candy Canes", "Gummy Bears":"Gummy Bears", "Cookie Dough":"Cookie Dough"}
    else: 
        tab_map = {"Safe Haven":"Safe Haven", "Stabilization":"Stabilization", "Drop-in Center":"Drop-in Center", "Outreach Team ":"Outreach Team "}

    tabs = st.tabs(list(tab_map.keys()))

    default_cols = [
                    "ProgramName", 
                    "Completed", 
                    "Delayed_Entry", 
                    "%Reported"
                ]

    all_columns = [
        'Facility_Type', 
        'ProgramName', 
        'PA', 
        'Completed', 
        'No_of_Weeks',
        'Delayed_Entry', 
        '%Reported'
    ]

    st.sidebar.header("Table Settings")
    selected_columns =  st.sidebar.multiselect(
        "Select columns to display", 
        options=all_columns, 
        default=default_cols
    )

    for tab_name, tab in zip(tab_map.keys(), tabs):
        with tab:
            df_to_show = facility_dict.get(tab_map[tab_name])    
            if df_to_show is not None:
                st.write(f"**{tab_name} Report View**")
                # truncate long text
                df_display = df_to_show.copy()
                filtered_table = df_display[selected_columns]

                for col in filtered_table.select_dtypes(include="object"):
                    filtered_table[col] = filtered_table[col].apply(lambda x: x if len(x)<=50 else x[:50]+"...")

                # auto-height
                row_height = 35
                table_height = min(600, row_height * len(df_display))
                st.dataframe(filtered_table, height=table_height, use_container_width=True)
            else:
                st.warning(f"No data for {tab_name}")
    
else: 
    filtered_df = compliance

    from utils import pivot_late_submissions, pivot_report_status, pivot_weeks_by_facility, build_reporting_tables, get_table_height
    data = filtered_df.copy()

    st.sidebar.header("Filters")

    type_list = sorted(data['Facility_Type'].dropna().unique())
    selected_type = st.sidebar.selectbox(
        "Program Type", 
        options=['All'] + type_list
    )

    df_select = data
    if selected_type != 'All':
        df_select = df_select[df_select['Facility_Type']== selected_type]
    
    pa_list = sorted(data['PA'].dropna().unique())
    selected_pa = st.sidebar.selectbox(
        "Filter by PA",
        options=['All'] + pa_list
    )

    program_list = sorted(df_select['List_of_Sites_SHS_Portfolio'].dropna().unique())

    selected_name = st.sidebar.selectbox(
        "Program Name", 
        options=['All'] + program_list
    )

    if selected_type != 'All':
        data = data[
            data['Facility_Type']==selected_type
        ]
        if selected_name != 'All':
            data = data[
                data['List_of_Sites_SHS_Portfolio'] == selected_name
            ]
        if selected_pa != 'All':
            data = data[
                data['PA'] == selected_pa
            ]
        if data.empty: 
            st.write("No data returned for selected filteres. Please drop all filteres and try again.")
            st.stop()
        else:
            pass
    
    else: 
        if selected_name != 'All':
            data = data[
                data['List_of_Sites_SHS_Portfolio'] == selected_name
            ]
        if selected_pa != 'All':
            data = data[
                data['PA'] == selected_pa
            ]
        if data.empty: 
            st.write("No data returned for selected filteres. Please drop all filteres and try again.")
            st.stop()
        else: 
            pass
            
    facility_dict = build_reporting_tables(data)

    if not facility_dict:
        st.warning("No data returned for selected filters. Try adjusting the date range or site.")
        st.stop()
    
    # Map friendly tab names to facility types
    tab_map = {"Safe Haven":"Safe Haven", "Stabilization":"Stabilization", "Drop-in Center":"Drop-in Center", "Outreach Team ":"Outreach Team "}

    tabs = st.tabs(list(tab_map.keys()))

    default_cols = [
                    "ProgramName", 
                    "Completed", 
                    "Delayed_Entry", 
                    "%Reported"
                ]

    all_columns = [
        'Facility_Type', 
        'ProgramName', 
        'PA', 
        'Completed', 
        'No_of_Weeks',
        'Delayed_Entry', 
        '%Reported'
    ]

    st.sidebar.header("Table Settings")
    selected_columns =  st.sidebar.multiselect(
        "Select columns to display", 
        options=all_columns, 
        default=default_cols
    )

    for tab_name, tab in zip(tab_map.keys(), tabs):
        with tab:
            df_to_show = facility_dict.get(tab_map[tab_name])    
            if df_to_show is not None:
                st.write(f"**{tab_name} Report View**")
                # truncate long text
                df_display = df_to_show.copy()
                filtered_table = df_display[selected_columns]

                for col in filtered_table.select_dtypes(include="object"):
                    filtered_table[col] = filtered_table[col].apply(lambda x: x if len(x)<=50 else x[:50]+"...")

                # auto-height
                row_height = 35
                table_height = min(600, row_height * len(df_display))
                st.dataframe(filtered_table, height=table_height, use_container_width=True)
            else:
                st.warning(f"No data for {tab_name}")
