import streamlit as st
from pages.auth import init_session_state, login_page, signup_page, auth_required, logout
from pages.chatbot import show_chatbot
from pages.yield_prediction import show_yield_prediction
from pages.admin import show_admin_panel

st.set_page_config(
    page_title="Agricultural Assistant",
    page_icon="🌾",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Enhanced CSS with improved styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4CAF50;
        --primary-light: rgba(76, 175, 80, 0.1);
        --primary-dark: #388E3C;
        --accent-color: #FFC107;
        --warning-color: #FFA726;
        --danger-color: #EF5350;
        --background-card: rgba(255, 255, 255, 0.05);
        --border-radius: 12px;
        --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* General Styles */
    body {
        color: var(--text-color);
        background-color: var(--background-color);
    }
    
    /* Hide Streamlit's default header in sidebar */
    #MainMenu, [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 30px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-dark) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Card styling */
    .card, .feature-card {
        background-color: var(--background-card);
        border-radius: var(--border-radius);
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid var(--primary-color);
        box-shadow: var(--box-shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover, .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Improve contrast for text in dark mode */
    .feature-card h2, .feature-card h3, .card-header {
        color: var(--primary-color);
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .feature-card p, .feature-card ul {
        color: var(--text-color);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.2);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar .stTitle, [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--primary-color);
        font-weight: bold;
    }
    
    /* Input fields and select boxes */
    .stSelectbox, .stTextInput>div>div {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: var(--border-radius);
        margin-bottom: 15px;
    }
    
    /* Metrics styling */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: var(--border-radius);
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary-color) !important;
    }
    
    /* Header styling */
    h1, .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        color: var(--primary-color);
        text-align: center;
        padding: 20px;
    }
    
    h3, h4 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
    }
    
    /* Divider */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), transparent);
        margin: 20px 0;
        border-radius: 3px;
    }
    
    /* Icon styling */
    .icon {
        vertical-align: middle;
        margin-right: 8px;
    }
    
    /* Illustration placeholder */
    .illustration-placeholder {
        background: linear-gradient(135deg, var(--primary-light), rgba(255, 255, 255, 0.05));
        border-radius: var(--border-radius);
        padding: 20px;
        text-align: center;
        margin: 10px 0 20px 0;
        border: 1px dashed var(--primary-color);
    }
    
    .illustration-icon {
        font-size: 3rem;
        color: var(--primary-color);
        margin-bottom: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 0.8em;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 2.5rem; color: #4CAF50; margin-bottom: 10px;">🌾</div>
        <h2 style="color: #4CAF50; margin-bottom: 20px;">Smart Agriculture</h2>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Show different navigation based on authentication status
    if st.session_state.is_authenticated:
        selected_page = st.selectbox(
            "Navigation",
            ["Home", "Yield Prediction", "Agricultural Assistant", "Admin Panel"]
        )
        
        # Add logout button
        if st.button("Logout"):
            logout()
    else:
        selected_page = st.selectbox(
            "Navigation",
            ["Login", "Sign Up"]
        )
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding: 20px 0; font-size: 0.8em; color: rgba(255, 255, 255, 0.7); text-align: center;">
        <p>Powered by AI & ML</p>
        <p>© 2025 Smart Agriculture</p>
    </div>
    """, unsafe_allow_html=True)

# Page routing
if selected_page == "Login":
    login_page()
elif selected_page == "Sign Up":
    signup_page()
else:
    # Protected routes
    @auth_required
    def show_home():
        st.markdown("<h1 class='main-header'>🌾 Smart Agriculture Platform</h1>", unsafe_allow_html=True)
        
        # Welcome message with username
        st.markdown(f"""
        <div class='card'>
            <h2 class='card-header'>Welcome {st.session_state.user['username']}!</h2>
            <p>Your all-in-one solution for modern farming and agricultural management. Leverage the power of 
            artificial intelligence and machine learning to optimize your agricultural practices.</p>
            <div class="divider"></div>
            <p><span style="color: #4CAF50;">✓</span> Data-driven farming decisions</p>
            <p><span style="color: #4CAF50;">✓</span> AI-powered crop analysis</p>
            <p><span style="color: #4CAF50;">✓</span> Precision agriculture tools</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main illustration
        st.markdown("""
        <div class="illustration-placeholder" style="height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div class="illustration-icon" style="font-size: 4rem;">🌱</div>
            <h3 style="color: var(--primary-color);">Transforming Agriculture with Technology</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Features section
        st.markdown("<h2 style='color: #4CAF50; margin: 30px 0 20px 0;'>Our Features</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='feature-card'>
                <h3><span class="icon">🎯</span> Yield Prediction</h3>
                <p>Advanced machine learning models to predict crop yields based on various parameters:</p>
                <ul>
                    <li><b>Multi-model ensemble</b> predictions for accuracy</li>
                    <li><b>Crop-specific</b> recommendations</li>
                    <li><b>Weather and soil</b> condition analysis</li>
                    <li><b>Uncertainty estimation</b> with confidence levels</li>
                </ul>
                <div style="text-align: center; margin-top: 20px;">
                    <div class="illustration-icon">📊</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='feature-card'>
                <h3><span class="icon">🤖</span> Agricultural Assistant</h3>
                <p>AI-powered chatbot to assist with:</p>
                <ul>
                    <li><b>Crop disease</b> identification and treatment</li>
                    <li><b>Pest control</b> recommendations</li>
                    <li><b>Best farming</b> practices and techniques</li>
                    <li><b>Real-time image</b> analysis of plants</li>
                </ul>
                <div style="text-align: center; margin-top: 20px;">
                    <div class="illustration-icon">💬</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # How it works section
        st.markdown("<h2 style='color: #4CAF50; margin: 30px 0 20px 0;'>How It Works</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='card' style="text-align: center;">
                <div class="illustration-icon">📝</div>
                <h3 style="margin: 10px 0;">Input Data</h3>
                <p>Enter your farming parameters or upload images of your crops</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='card' style="text-align: center;">
                <div class="illustration-icon">⚙️</div>
                <h3 style="margin: 10px 0;">AI Processing</h3>
                <p>Our advanced algorithms analyze your data for insights</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class='card' style="text-align: center;">
                <div class="illustration-icon">✅</div>
                <h3 style="margin: 10px 0;">Get Results</h3>
                <p>Receive actionable recommendations and predictions</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="footer">
            <div class="divider"></div>
            <p>Smart Agriculture Platform | Powered by Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)


    # Route to the appropriate page
    if selected_page == "Home":
        show_home()
    elif selected_page == "Yield Prediction":
        show_yield_prediction()
    elif selected_page == "Agricultural Assistant":
        show_chatbot()
    elif selected_page == "Admin Panel":
        show_admin_panel()