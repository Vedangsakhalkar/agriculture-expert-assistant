# pages/yield_prediction.py
import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.express as px

# Custom CSS
def local_css():
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
        
        /* Card styling */
        .card {
            background-color: var(--background-card);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 20px;
            border-left: 5px solid var(--primary-color);
            box-shadow: var(--box-shadow);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .card-header {
            color: var(--primary-color);
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 30px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Form inputs */
        .stSelectbox, .stNumberInput {
            margin-bottom: 15px;
        }
        
        /* Metrics styling */
        .metric-card {
            background-color: var(--background-card);
            border-radius: var(--border-radius);
            padding: 20px;
            text-align: center;
            box-shadow: var(--box-shadow);
            height: 100%;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        /* Header styling */
        h1 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            letter-spacing: 1px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        h3, h4 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }
        
        /* Results styling */
        .result-item {
            background-color: var(--background-card);
            border-radius: var(--border-radius);
            padding: 15px;
            margin: 10px 0;
            border-left: 5px solid var(--primary-color);
            transition: transform 0.3s ease;
        }
        
        .result-item:hover {
            transform: translateY(-3px);
        }
        
        /* Icon styling */
        .icon {
            vertical-align: middle;
            margin-right: 8px;
        }
        
        /* Divider */
        .divider {
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), transparent);
            margin: 20px 0;
            border-radius: 3px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            font-size: 0.8em;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 30px;
        }
        
        /* Streamlit default element overrides */
        div.block-container {
            padding-top: 2rem;
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
    </style>
    """, unsafe_allow_html=True)

# Cache models
@st.cache_resource
def load_models():
    try:
        models = {
            'rf_model': joblib.load(r"C:/Users/vedan/OneDrive/Desktop/ariculture/models/rf_model.pkl"),
            'gb_model': joblib.load(r"C:/Users/vedan/OneDrive/Desktop/ariculture/models/gb_model.pkl"),
            'scaler': joblib.load(r"C:/Users/vedan/OneDrive/Desktop/ariculture/models/scaler.pkl"),
            'label_encoders': joblib.load(r"C:/Users/vedan/OneDrive/Desktop/ariculture/models/label_encoders.pkl")
        }
        return models
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None

def predict_crop_yield(state, season, crop, area, rainfall, fertilizer, pesticide, models):
    try:
        state_enc = models['label_encoders']['State'].transform([state])[0]
        season_enc = models['label_encoders']['Season'].transform([season])[0]
        crop_enc = models['label_encoders']['Crop'].transform([crop])[0]
        
        features = np.array([[crop_enc, season_enc, state_enc, area, rainfall, fertilizer, pesticide]])
        features_scaled = models['scaler'].transform(features)
        
        rf_pred = models['rf_model'].predict(features_scaled)[0]
        gb_pred = models['gb_model'].predict(features_scaled)[0]
        
        ensemble_pred = (rf_pred + gb_pred) / 2
        uncertainty = abs(rf_pred - gb_pred) / 2
        relative_uncertainty = (uncertainty / ensemble_pred) * 100
        
        return {
            'rf_prediction': rf_pred,
            'gb_prediction': gb_pred,
            'ensemble_prediction': ensemble_pred,
            'uncertainty': uncertainty,
            'relative_uncertainty': relative_uncertainty
        }
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

def predict_best_crops(state, season, area, rainfall, fertilizer, pesticide, models):
    predictions = []
    for crop in models['label_encoders']['Crop'].classes_:
        result = predict_crop_yield(state, season, crop, area, rainfall, fertilizer, pesticide, models)
        if result:
            predictions.append({
                'crop': crop,
                'yield': result['ensemble_prediction'],
                'uncertainty': result['uncertainty']
            })
    return sorted(predictions, key=lambda x: x['yield'], reverse=True)[:5]

def show_yield_prediction():
    # Apply custom CSS
    local_css()
    
    # Header section
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌾 Agricultural Yield Prediction</h1>", unsafe_allow_html=True)
    
    # Introduction card
    st.markdown("""
        <div class="card">
            <h4 class="card-header">Smart Yield Prediction System</h4>
            <p>This advanced system uses ensemble machine learning models to predict crop yields based on various environmental 
            and agricultural factors. Enter your parameters below to get accurate yield predictions and crop recommendations.</p>
            <div class="divider"></div>
            <p><span style="color: #4CAF50;">✓</span> Data-driven predictions for optimal farming decisions</p>
            <p><span style="color: #4CAF50;">✓</span> Compare different crops for your specific conditions</p>
            <p><span style="color: #4CAF50;">✓</span> Get insights on expected yields with confidence levels</p>
        </div>
    """, unsafe_allow_html=True)
    
    models = load_models()
    if not models:
        st.error("Failed to load models. Please check model files.")
        return
    
    # Main content columns
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3 class="card-header"><span class="icon">📊</span> Input Parameters</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display illustration placeholder instead of Lottie animation
        st.markdown("""
            <div class="illustration-placeholder">
                <div class="illustration-icon">🌱</div>
                <p>Enter your farming parameters below to get started</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("prediction_form"):
            states = models['label_encoders']['State'].classes_
            state = st.selectbox("🏞️ Select State", states)
            
            seasons = models['label_encoders']['Season'].classes_
            season = st.selectbox("🌤️ Select Season", seasons)
            
            crops = models['label_encoders']['Crop'].classes_
            crop = st.selectbox("🌱 Select Crop", crops)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            area = st.number_input("🔍 Area (hectares)", 
                                 min_value=0.1, 
                                 max_value=10000.0, 
                                 value=100.0,
                                 help="Enter the total area of cultivation in hectares")
            
            rainfall = st.number_input("💧 Rainfall (mm)", 
                                     min_value=0.0, 
                                     max_value=5000.0, 
                                     value=1000.0,
                                     help="Enter the expected rainfall in millimeters")
            
            fertilizer = st.number_input("🧪 Fertilizer (kg/ha)", 
                                       min_value=0.0, 
                                       max_value=1000.0, 
                                       value=100.0,
                                       help="Enter the amount of fertilizer to be used in kg/ha")
            
            pesticide = st.number_input("🧫 Pesticide (kg/ha)", 
                                      min_value=0.0, 
                                      max_value=100.0, 
                                      value=10.0,
                                      help="Enter the amount of pesticide to be used in kg/ha")
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                single_predict = st.form_submit_button("🔮 Predict Yield")
            with col1_2:
                best_crops = st.form_submit_button("🏆 Find Best Crops")
    
    with col2:
        # Display placeholder when no results are shown
        if not single_predict and not best_crops:
            st.markdown("""
                <div class="card">
                    <h3 class="card-header"><span class="icon">📈</span> Yield Analysis</h3>
                    <p>Submit the form to see prediction results here</p>
                </div>
                <div class="illustration-placeholder" style="height: 300px; display: flex; flex-direction: column; justify-content: center;">
                    <div class="illustration-icon">📊</div>
                    <h3 style="color: var(--primary-color);">Your Prediction Results Will Appear Here</h3>
                    <p>Fill in the parameters and click one of the prediction buttons</p>
                </div>
            """, unsafe_allow_html=True)
        
        if single_predict:
            results = predict_crop_yield(state, season, crop, area, rainfall, fertilizer, pesticide, models)
            
            if results:
                st.markdown(f"""
                    <div class="card">
                        <h3 class="card-header"><span class="icon">🌾</span> Prediction Results for {crop}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                pred_col1, pred_col2, pred_col3 = st.columns(3)
                
                with pred_col1:
                    st.markdown("""
                        <div class="metric-card">
                            <h4 style='color: #4CAF50;'><span class="icon">🌲</span> Random Forest</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.metric(
                        "Prediction",
                        f"{results['rf_prediction']:.2f} tons/ha"
                    )
                
                with pred_col2:
                    st.markdown("""
                        <div class="metric-card">
                            <h4 style='color: #4CAF50;'><span class="icon">🚀</span> Gradient Boosting</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.metric(
                        "Prediction",
                        f"{results['gb_prediction']:.2f} tons/ha"
                    )
                
                with pred_col3:
                    st.markdown("""
                        <div class="metric-card">
                            <h4 style='color: #4CAF50;'><span class="icon">⭐</span> Ensemble Prediction</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.metric(
                        "Final Prediction",
                        f"{results['ensemble_prediction']:.2f} tons/ha",
                        f"±{results['relative_uncertainty']:.1f}%"
                    )
                
                # Additional insights
                st.markdown("""
                    <div class="card" style="margin-top: 20px;">
                        <h4 class="card-header"><span class="icon">💡</span> Prediction Insights</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                uncertainty_level = "Low" if results['relative_uncertainty'] < 10 else "Moderate" if results['relative_uncertainty'] < 20 else "High"
                uncertainty_color = "#4CAF50" if uncertainty_level == "Low" else "#FFA726" if uncertainty_level == "Moderate" else "#EF5350"
                
                # Create gauge chart for uncertainty
                fig_gauge = px.bar(
                    x=["Confidence"], 
                    y=[100 - min(results['relative_uncertainty'], 100)],
                    labels={"x": "", "y": "Confidence Level (%)"},
                    range_y=[0, 100],
                    color_discrete_sequence=["#4CAF50" if uncertainty_level == "Low" else "#FFA726" if uncertainty_level == "Moderate" else "#EF5350"]
                )
                fig_gauge.update_layout(
                    height=200,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='var(--text-color)',
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                
                insight_col1, insight_col2 = st.columns([2, 1])
                
                with insight_col1:
                    st.markdown(f"""
                        <div class="result-item">
                            <p>
                            <span style="color: {uncertainty_color}; font-weight: bold;">● {uncertainty_level} Uncertainty</span> (±{results['relative_uncertainty']:.1f}%)<br>
                            <span style="color: #4CAF50;">● Predicted yield range:</span> {results['ensemble_prediction'] - results['uncertainty']:.2f} to {results['ensemble_prediction'] + results['uncertainty']:.2f} tons/ha<br>
                            <span style="color: #4CAF50;">● Land area:</span> {area:.1f} hectares<br>
                            <span style="color: #4CAF50;">● Expected rainfall:</span> {rainfall:.0f}mm
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with insight_col2:
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Recommendations based on results
                st.markdown(f"""
                    <div class="card" style="margin-top: 20px;">
                        <h4 class="card-header"><span class="icon">🔍</span> Recommendations</h4>
                        <p>Based on the prediction results for {crop} in {state} during {season} season:</p>
                        <ul>
                            <li>Expected yield of <b>{results['ensemble_prediction']:.2f} tons/ha</b> is 
                            {" promising" if results['ensemble_prediction'] > 2 else " moderate" if results['ensemble_prediction'] > 1 else " relatively low"}.</li>
                            <li>Consider {"increasing" if results['ensemble_prediction'] < 2 else "maintaining"} fertilizer application for optimal results.</li>
                            <li>Monitor weather patterns closely as rainfall significantly impacts yield.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
        
        elif best_crops:
            results = predict_best_crops(state, season, area, rainfall, fertilizer, pesticide, models)
            
            st.markdown("""
                <div class="card">
                    <h3 class="card-header"><span class="icon">🏆</span> Top 5 Recommended Crops</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Create DataFrame for visualization
            df = pd.DataFrame(results)
            
            # Create bar chart with improved styling
            fig = px.bar(df, 
                        x='crop', 
                        y='yield',
                        error_y='uncertainty',
                        title='Expected Yield by Crop',
                        labels={'crop': 'Crop', 'yield': 'Expected Yield (tons/ha)'},
                        color_discrete_sequence=['#4CAF50'])
            
            # Update layout for dark mode compatibility and better styling
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='var(--text-color)',
                title_font_size=20,
                title_font_family="Helvetica Neue",
                title_font_color="#4CAF50",
                legend_title_font_color="#4CAF50",
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)', title_font_size=14)
            fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)', title_font_size=14)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed results with improved styling
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #4CAF50; margin-bottom: 20px;'><span class='icon'>📋</span> Detailed Crop Analysis</h4>", unsafe_allow_html=True)
            
            # Create two columns for crop details
            crop_col1, crop_col2 = st.columns(2)
            
            for i, pred in enumerate(results, 1):
                uncertainty_level = "Low" if (pred['uncertainty'] / pred['yield'] * 100) < 10 else "Moderate" if (pred['uncertainty'] / pred['yield'] * 100) < 20 else "High"
                uncertainty_color = "#4CAF50" if uncertainty_level == "Low" else "#FFA726" if uncertainty_level == "Moderate" else "#EF5350"
                
                crop_card = f"""
                    <div class="result-item">
                        <h4 style='color: #4CAF50;'>{i}. {pred['crop']}</h4>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <p><span style="color: #4CAF50;">● Expected Yield:</span> <b>{pred['yield']:.2f} tons/ha</b></p>
                                <p><span style="color: {uncertainty_color};">● Uncertainty:</span> ±{(pred['uncertainty'] / pred['yield'] * 100):.1f}% ({uncertainty_level})</p>
                            </div>
                            <div style="font-size: 2em; color: #4CAF50;">
                                {'🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else '🏅'}
                            </div>
                        </div>
                    </div>
                """
                
                if i <= 3:
                    with crop_col1:
                        st.markdown(crop_card, unsafe_allow_html=True)
                else:
                    with crop_col2:
                        st.markdown(crop_card, unsafe_allow_html=True)
            
            # Comparison summary
            st.markdown("""
                <div class="card" style="margin-top: 20px;">
                    <h4 class="card-header"><span class="icon">📊</span> Comparison Summary</h4>
                    <p>The top recommended crop shows a yield potential that is 
                    <span style="color: #4CAF50; font-weight: bold;">
                    {:.1f}%
                    </span> higher than the average of all analyzed crops.</p>
                    <p>Consider these recommendations along with market prices, labor requirements, and your specific farming capabilities.</p>
                </div>
            """.format((results[0]['yield'] / (sum(r['yield'] for r in results) / len(results)) - 1) * 100), unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <div class="divider"></div>
            <p>Agricultural Yield Prediction System | Powered by Machine Learning</p>
        </div>
    """, unsafe_allow_html=True)