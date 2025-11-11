import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_classic.agents.agent_types import AgentType
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="Langchain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 Langchain: Chat with SQL DB")

LOCALDB= "USE_LOCALDB"
MYSQL= "USE_MYSQL"

radio_opt = ["Use SQLite 3 Database- Student.db", "Connect to your SQL Database"]

selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat with", options=radio_opt)
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide My SQL Host")
    mysql_user = st.sidebar.text_input("MYSQL User")
    mysql_password = st.sidebar.text_input("MySQL password", type="password")
    mysql_db = st.sidebar.text_input("MySQL database")
else:
    db_uri = LOCALDB


api_key = st.sidebar.text_input(label="GROQ API Key", type="password")

if not db_uri:
    st.info("Please enter the database information and URL")

if not api_key:
    st.info("Please add the groq api key")

## LLM model
ChatGroq(groq_api_key=api_key, model="llama-3.3-70b-versatile", streaming=True)

@st.cache_resourse(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_db and mysql_host and mysql_password and mysql_user):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    
if db_uri==MYSQL:
    db=configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db=configure_db(db_uri)

