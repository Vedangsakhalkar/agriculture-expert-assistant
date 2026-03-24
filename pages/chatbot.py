import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key securely
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("API key not found. Please add it to your .env file.")
    st.stop()

# Configure Google AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_agri_response(question, image=None):
    if image:
        prompt = f"""You are an agricultural expert assistant. Analyze this image and provide detailed information
        about what you see. If it shows any plant diseases, pests, or issues, provide identification and treatment
        recommendations. If it shows healthy crops or agricultural practices, provide relevant insights and tips.
        
        Additional Question: {question}
        """
        try:
            response = model.generate_content([prompt, image])
            return response.text if response.text else "I apologize, but I couldn't analyze the image. Please try again."
        except Exception as e:
            return f"I apologize, but I encountered an error analyzing the image: {str(e)}"
    else:
        prompt = f"""You are an agricultural expert assistant. Please provide accurate and helpful information 
        about farming, crops, soil management, irrigation, pest control, and other agricultural topics. 
        Only answer questions related to agriculture. If the question is not about agriculture, 
        politely inform that you can only assist with agricultural queries.

        Question: {question}
        """
        try:
            response = model.generate_content(prompt)
            return response.text if response.text else "I apologize, but I couldn't generate a response. Please try rephrasing your question."
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

def show_chatbot():
    # Header section
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 Agricultural Expert Assistant</h1>", unsafe_allow_html=True)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Introduction card
    st.markdown("""
        <div class="card">
            <h4 class="card-header"><span class="icon">🌱</span> AI-Powered Agricultural Assistant</h4>
            <p>Ask me anything about agriculture! I can help with crop management, disease identification, 
            best practices, and more. You can also upload an image for analysis.</p>
            <div class="divider"></div>
            <p><span style="color: #4CAF50;">✓</span> Get expert advice on farming practices</p>
            <p><span style="color: #4CAF50;">✓</span> Identify plant diseases and pests</p>
            <p><span style="color: #4CAF50;">✓</span> Receive personalized recommendations</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    # Right column - Features and image upload
    with col2:
        st.markdown("""
            <div class="card">
                <h3 class="card-header"><span class="icon">📋</span> Features</h3>
                <ul>
                    <li><b>Image Analysis</b> - Upload crop photos</li>
                    <li><b>Disease Detection</b> - Identify plant issues</li>
                    <li><b>Farming Advice</b> - Get best practices</li>
                    <li><b>Pest Control</b> - Solutions for infestations</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Image upload section
        st.markdown("""
            <div class="card">
                <h3 class="card-header"><span class="icon">🖼️</span> Image Analysis</h3>
                <p>Upload an image of your crops or plants for AI analysis</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
        uploaded_image = None
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                uploaded_image = image
                
                st.markdown("""
                    <div class="result-item">
                        <p><span style="color: #4CAF50;">✓</span> <b>Image uploaded successfully!</b></p>
                        <p>Ask a question about this image in the chat to get an analysis.</p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error opening image: {e}")
        else:
            # Placeholder when no image is uploaded
            st.markdown("""
                <div class="illustration-placeholder" style="height: 150px; display: flex; flex-direction: column; justify-content: center;">
                    <div class="illustration-icon">📷</div>
                    <p>Upload an image for analysis</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Left column - Chat interface
    with col1:
        # Chat container with improved styling
        chat_container = st.container()
        
        with chat_container:
            if not st.session_state.chat_history:
                # Empty state illustration
                st.markdown("""
                    <div class="illustration-placeholder" style="height: 200px; display: flex; flex-direction: column; justify-content: center;">
                        <div class="illustration-icon">💬</div>
                        <h3 style="color: var(--primary-color);">Start a Conversation</h3>
                        <p>Ask me anything about agriculture!</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Display chat messages with improved styling
                for role, message in st.session_state.chat_history:
                    if role == "user":
                        st.markdown(f"""
                            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                                <div style="background-color: rgba(76, 175, 80, 0.1); padding: 12px 16px; border-radius: 18px 18px 0 18px; max-width: 80%; box-shadow: var(--box-shadow);">
                                    <p style="margin: 0; color: var(--text-color);"><b>You:</b> {message}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="display: flex; margin: 10px 0;">
                                <div style="background-color: var(--background-card); padding: 12px 16px; border-radius: 18px 18px 18px 0; max-width: 80%; border-left: 3px solid var(--primary-color); box-shadow: var(--box-shadow);">
                                    <p style="margin: 0 0 5px 0; color: var(--primary-color);"><b>🤖 Assistant</b></p>
                                    <p style="margin: 0; color: var(--text-color);">{message}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # Input area with improved styling
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        with st.container():
            user_question = st.text_input("", 
                                        placeholder="Ask about crops, farming, or the uploaded image...",
                                        key="user_input")
            
            col1_1, col1_2, col1_3 = st.columns([2, 1, 1])
            with col1_1:
                if st.button("🔍 Ask Question", key="ask_button"):
                    if user_question:
                        # Show a spinner while processing
                        with st.spinner("Thinking..."):
                            if uploaded_image:
                                bot_response = get_agri_response(user_question, uploaded_image)
                                st.session_state.chat_history.append(("user", f"[Image Uploaded] {user_question}"))
                            else:
                                bot_response = get_agri_response(user_question)
                                st.session_state.chat_history.append(("user", user_question))
                            st.session_state.chat_history.append(("bot", bot_response))
                        st.rerun()
            
            with col1_2:
                if st.button("🔄 New Chat", key="clear_button"):
                    st.session_state.chat_history = []
                    st.rerun()
            
            with col1_3:
                # Example questions button
                if st.button("💡 Examples", key="examples_button"):
                    st.markdown("""
                        <div class="card">
                            <h4 class="card-header">Example Questions</h4>
                            <ul>
                                <li>"How do I treat tomato leaf blight?"</li>
                                <li>"What are the best crops to grow in sandy soil?"</li>
                                <li>"How much water does corn need per week?"</li>
                                <li>"What are organic methods to control aphids?"</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Tips section at the bottom
        if not st.session_state.chat_history:
            st.markdown("""
                <div class="card" style="margin-top: 20px;">
                    <h4 class="card-header"><span class="icon">💡</span> Tips for Better Results</h4>
                    <ul>
                        <li>Be specific in your questions</li>
                        <li>Upload clear, well-lit images</li>
                        <li>Include your location for region-specific advice</li>
                        <li>Mention the growth stage of your plants</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <div class="divider"></div>
            <p>Agricultural Expert Assistant | Powered by Gemini AI</p>
        </div>
    """, unsafe_allow_html=True)
