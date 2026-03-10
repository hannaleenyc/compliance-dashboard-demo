# sql_load.py

import os
from dotenv import load_dotenv
import pandas as pd
from queries import GET_COMPLIANCE, GET_PMO_DATA, GET_REENTRY_DATA
import pyodbc

# Load variables from .env
load_dotenv('venv\\.env')

def get_connection(): 
    import os
    from dotenv import load_dotenv
    load_dotenv('venv\\.env')
    ## Connection parameters 
    server = os.getenv("DB_SERVER")
    driver = os.getenv("DB_DRIVER")
    ## Create connection string using Windows autentification. 
    conn_str = f'DRIVER={driver};SERVER={server};Trusted_Connection=yes; TrustServerCertificate=yes'
    return pyodbc.connect(conn_str)

def get_data(): 
    conn = get_connection()
    compliance = pd.read_sql(GET_COMPLIANCE, conn)
    pmo_data = pd.read_sql(GET_PMO_DATA, conn)
    reentry_data = pd.read_sql(GET_REENTRY_DATA, conn)
    return compliance, pmo_data, reentry_data
    
def get_csv():
    os.makedirs("data", exist_ok=True)
    try:
        compliance = pd.read_csv("data/compliance.csv")
        pmo_data = pd.read_csv("data/pmo_data.csv")
        reentry_data = pd.read_csv("data/reentry_data.csv")
        return compliance, pmo_data, reentry_data
    
    except Exception:
        ## Upload SQL data as csv to data. 
        compliance, pmo_data, reentry_data = get_data()
        compliance.to_csv("data\\compliance.csv")
        pmo_data.to_csv("data\\pmo_data.csv")
        reentry_data.to_csv("data\\reentry_data.csv")

        ## Load data from csv file to use.
        compliance = pd.read_csv("data/compliance.csv")
        pmo_data = pd.read_csv("data/pmo_data.csv")
        reentry_data = pd.read_csv("data/reentry_data.csv")
        return compliance, pmo_data, reentry_data
    

