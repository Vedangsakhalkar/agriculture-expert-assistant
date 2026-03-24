import streamlit as st
from database import Database
from pages.auth import auth_required

@auth_required
def show_admin_panel():
    """Display the admin panel with user management functionality."""
    st.markdown("<h1 class='main-header'>Admin Panel</h1>", unsafe_allow_html=True)
    
    # Check if the logged-in user is 'admin'
    if 'user' not in st.session_state or st.session_state.user['username'] != 'admin':
        st.error("You don't have permission to access this page.")
        return
    
    st.markdown("<h2>User Management</h2>", unsafe_allow_html=True)
    
    # Get all users from database
    db = Database()
    users = db.get_all_users()
    
    if not users:
        st.info("No users found in the database.")
    else:
        # Display users in a table
        st.markdown("<h3>Registered Users</h3>", unsafe_allow_html=True)
        
        # Create a DataFrame for better display
        import pandas as pd
        
        # Convert users to a list of dictionaries
        user_data = [{
            "ID": user[0],
            "Username": user[1],
            "Email": user[2]
        } for user in users]
        
        # Create and display the DataFrame
        df = pd.DataFrame(user_data)
        st.dataframe(df, use_container_width=True)
        
        # Display total count
        st.markdown(f"<p>Total Users: {len(users)}</p>", unsafe_allow_html=True)