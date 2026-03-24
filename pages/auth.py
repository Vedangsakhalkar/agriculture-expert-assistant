import streamlit as st
import re
from database import Database

def init_session_state():
    """Initialize session state variables."""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, ""

def login_page():
    """Display the login page."""
    st.markdown("<h1 class='main-header'>Login</h1>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields")
                return
                
            db = Database()
            user = db.verify_user(username, password)
            
            if user:
                st.session_state.user = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2]
                }
                st.session_state.is_authenticated = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    # st.markdown("""
    #     <div style='text-align: center; margin-top: 20px;'>
    #         Don't have an account? <a href="?page=signup">Sign up</a>
    #     </div>
    # """, unsafe_allow_html=True)

def signup_page():
    """Display the signup page."""
    st.markdown("<h1 class='main-header'>Sign Up</h1>", unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill in all fields")
                return
                
            if not validate_email(email):
                st.error("Please enter a valid email address")
                return
                
            is_valid_password, password_error = validate_password(password)
            if not is_valid_password:
                st.error(password_error)
                return
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return
                
            db = Database()
            
            if db.user_exists(username=username):
                st.error("Username already exists")
                return
                
            if db.user_exists(email=email):
                st.error("Email already registered")
                return
                
            if db.create_user(username, password, email):
                st.success("Account created successfully! Please login.")
                st.markdown('<meta http-equiv="refresh" content="2; url=?page=login">', unsafe_allow_html=True)
            else:
                st.error("An error occurred. Please try again.")
    
    # st.markdown("""
    #     <div style='text-align: center; margin-top: 20px;'>
    #         Already have an account? <a href="?page=login">Login</a>
    #     </div>
    # """, unsafe_allow_html=True)

def auth_required(func):
    """Decorator to require authentication for protected pages."""
    def wrapper(*args, **kwargs):
        init_session_state()
        if not st.session_state.is_authenticated:
            login_page()
            return
        return func(*args, **kwargs)
    return wrapper

def logout():
    """Log out the current user."""
    st.session_state.user = None
    st.session_state.is_authenticated = False
    st.rerun() 