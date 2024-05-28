import streamlit as st
import httpx
import pandas as pd
import plotly.express as px

# API base URL
BASE_URL = "https://paper-trading-71hl.onrender.com/api"

# Function to handle API key input and persistence
def handle_api_key():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    return st.text_input("Enter API Key", value=st.session_state.api_key)

def handle_team():
    if 'team' not in st.session_state:
        st.session_state.team = ''
    return st.text_input("Enter Team Name", value=st.session_state.team)

# Functions to call API endpoints with exception handling
def fetch_portfolio():
    try:
        response = httpx.get(f"{BASE_URL}/portfolio", headers={"api-key": st.session_state.api_key}, timeout=20.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.error(f"Error fetching portfolio data: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def fetch_transaction():
    try:
        response = httpx.get(f"{BASE_URL}/transaction", headers={"api-key": st.session_state.api_key}, timeout=60.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.error(f"Error fetching transaction data: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def fetch_user():
    try:
        response = httpx.get(f"{BASE_URL}/user", headers={"api-key": st.session_state.api_key}, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.error(f"Error fetching user data: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def fetch_dashboard():
    try:
        response = httpx.get(f"{BASE_URL}/dashboard", headers={"team": st.session_state.team}, timeout=60.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.error(f"Error fetching dashboard data: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Function to display portfolio data
def portfolio_page():
    cols = st.columns(2)
    
    with cols[0]:
        api_key = handle_api_key()
        if api_key and api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
    
    with cols[1]:
        cols[1].markdown("<div style='width: 1px; height: 28px'></div>", unsafe_allow_html=True)
        load_portfolio = False
        if st.button("Load Data"):
            load_portfolio = True
    
    if api_key == '':
        st.write("Please enter an API key to fetch portfolio data")
        return
    
    if load_portfolio:
        # Fetch user data
        if 'user_data' not in st.session_state:
            user_data = fetch_user()
            if user_data:
                st.session_state.user_data = user_data
                
        # Display user data
        if 'user_data' in st.session_state:
            user_data = st.session_state.user_data
            col1 = st.columns(3)
            
            with col1[0]:
                st.write(f"Name: {user_data['name']}")
            with col1[1]:
                st.write(f"Team: {user_data['team']}")
            with col1[2]:
                st.write(f"Balance: {user_data['balance']}")
            
        else:
            st.write("Failed to load user data.")
        
        data = fetch_portfolio()
        if data:
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.write("No portfolio data found")
        load_portfolio = False

# Function to display transaction data
def transaction_page():
    cols = st.columns(2)
    
    with cols[0]:
        api_key = handle_api_key()
        if api_key and api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
    
    with cols[1]:
        cols[1].markdown("<div style='width: 1px; height: 28px'></div>", unsafe_allow_html=True)
        load_transaction = False
        if st.button("Load Data"):
            load_transaction = True
            
    if api_key == '':
        st.write("Please enter an API key to fetch transaction data")
        return
    
    if load_transaction:
        if 'user_data' not in st.session_state:
            user_data = fetch_user()
            if user_data:
                st.session_state.user_data = user_data
                
        # Display user data
        if 'user_data' in st.session_state:
            user_data = st.session_state.user_data
            col1 = st.columns(3)
            
            with col1[0]:
                st.write(f"Name: {user_data['name']}")
            with col1[1]:
                st.write(f"Team: {user_data['team']}")
            with col1[2]:
                st.write(f"Balance: {user_data['balance']}")
            
        else:
            st.write("Failed to load user data.")
            
        data = fetch_transaction()
        if data:
            df = pd.DataFrame(data)
            # Convert the time format from ISO 8601 to a more readable format
            if 'Time' in df.columns:
                df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Display table
            st.table(df)
            
            # Plot transaction data
            if 'Time' in df.columns and 'After_balance' in df.columns:
                fig = px.line(df, x='Time', y='After_balance', title='Transaction Balance Over Time')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Unable to plot transaction data: 'Time' or 'Balance' column is missing.")
        else:
            st.write("No transaction data found")
        load_transaction = False

# Function to display dashboard data
def dashboard_page():
    cols = st.columns(2)
    
    with cols[0]:
        team = handle_team()
        if team and team != st.session_state.team:
            st.session_state.team = team
    
    with cols[1]:
        cols[1].markdown("<div style='width: 1px; height: 28px'></div>", unsafe_allow_html=True)
        load_dashboard = False
        if st.button("Load Data"):
            load_dashboard = True
    
    if team == '':
        st.write("Please enter a team name to fetch dashboard data")
        return

    if load_dashboard:
        data = fetch_dashboard()
        if data:
            df = pd.DataFrame(data)
            # Sort the DataFrame by 'Balance' in decreasing order and add a 'Rank' column
            if 'Balance' in df.columns:
                df = df.sort_values(by='Balance', ascending=False)
                df['Rank'] = df['Balance'].rank(ascending=False, method='min').astype(int)
            st.table(df)
        else:
            st.write("No dashboard data found")
        load_dashboard = False

st.header("Paper Trading Dashboard")

# Initialize current_page in session state if not already set
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Portfolio'

# Navigation buttons styled as tabs
tabs = st.container()

with tabs:
    col1, col2, col3 = st.columns(3)
    if col1.button('Portfolio', use_container_width=True):
        st.session_state.current_page = 'Portfolio'
    if col2.button('Transaction', use_container_width=True):
        st.session_state.current_page = 'Transaction'
    if col3.button('Competition', use_container_width=True):
        st.session_state.current_page = 'Competiton'

# Display content based on the current page
if st.session_state.current_page == 'Portfolio':
    st.subheader("Portfolio Dashboard")
    portfolio_page()
elif st.session_state.current_page == 'Transaction':
    st.subheader("Transaction Dashboard")
    transaction_page()
elif st.session_state.current_page == 'Competiton':
    st.subheader("Competition Dashboard")
    dashboard_page()
