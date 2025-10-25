import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("heart_model.pkl", "rb"))

# Page configuration
st.set_page_config(
    page_title="Heart Disease Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main .block-container {
        background-color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    .result-card {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .low-risk {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .high-risk {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<h1 class="main-title">❤️ Heart Disease Risk Predictor</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">AI-Powered Medical Analysis Tool</p>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/000000/heart-with-pulse.png",
        width=100
    )
    st.title("About")
    st.markdown("""
    This application uses **Machine Learning** to predict
    the likelihood of heart disease based on medical parameters.

    ### 📊 Model Performance
    - **Algorithm**: Logistic Regression
    - **Accuracy**: 88.5%
    - **Dataset**: Cleveland Heart Disease Database

    ### ⚠️ Important Notice
    This tool is for **educational purposes only** and should
    not replace professional medical diagnosis.

    ### 🏥 When to See a Doctor
    - Persistent chest pain
    - Shortness of breath
    - Irregular heartbeat
    - Family history of heart disease
    """)

    st.markdown("---")
    st.markdown("**Developed by**: Abhishek Chandra")

# Main content
st.markdown("### 📋 Enter Patient Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### 👤 **Personal Information**")
    age = st.number_input(
        "Age (years)",
        min_value=20,
        max_value=100,
        value=50
    )
    sex = st.selectbox("Sex", ["Male", "Female"])

    st.markdown("##### 💓 **Heart Rate**")
    thalach = st.number_input(
        "Maximum Heart Rate",
        min_value=70,
        max_value=210,
        value=150,
        help="Maximum heart rate achieved during exercise"
    )
    oldpeak = st.number_input(
        "ST Depression",
        min_value=0.0,
        max_value=6.0,
        value=1.0,
        step=0.1,
        help="ST depression induced by exercise"
    )

with col2:
    st.markdown("##### 🩺 **Clinical Measurements**")
    trestbps = st.number_input(
        "Resting Blood Pressure (mm Hg)",
        min_value=80,
        max_value=200,
        value=120
    )
    chol = st.number_input(
        "Cholesterol (mg/dl)",
        min_value=100,
        max_value=600,
        value=200
    )
    fbs = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl?",
        ["No", "Yes"]
    )

    st.markdown("##### 🫀 **Vessels**")
    ca = st.selectbox(
        "Major Vessels (0-4)",
        [0, 1, 2, 3, 4],
        help="Number of major vessels colored by fluoroscopy"
    )

with col3:
    st.markdown("##### 🏥 **Medical Tests**")
    cp = st.selectbox(
        "Chest Pain Type",
        [
            "Typical Angina",
            "Atypical Angina",
            "Non-anginal Pain",
            "Asymptomatic"
        ]
    )
    restecg = st.selectbox(
        "Resting ECG",
        [
            "Normal",
            "ST-T Wave Abnormality",
            "Left Ventricular Hypertrophy"
        ]
    )
    exang = st.selectbox(
        "Exercise Induced Angina?",
        ["No", "Yes"]
    )
    slope = st.selectbox(
        "ST Segment Slope",
        ["Upsloping", "Flat", "Downsloping"]
    )
    thal = st.selectbox(
        "Thalassemia",
        ["Normal", "Fixed Defect", "Reversible Defect"]
    )

# Convert inputs
sex_num = 1 if sex == "Male" else 0

cp_map = {
    "Typical Angina": 0,
    "Atypical Angina": 1,
    "Non-anginal Pain": 2,
    "Asymptomatic": 3
}
cp_num = cp_map[cp]

fbs_num = 1 if fbs == "Yes" else 0

restecg_map = {
    "Normal": 0,
    "ST-T Wave Abnormality": 1,
    "Left Ventricular Hypertrophy": 2
}
restecg_num = restecg_map[restecg]

exang_num = 1 if exang == "Yes" else 0

slope_map = {
    "Upsloping": 0,
    "Flat": 1,
    "Downsloping": 2
}
slope_num = slope_map[slope]

thal_map = {
    "Normal": 1,
    "Fixed Defect": 2,
    "Reversible Defect": 3
}
thal_num = thal_map[thal]

# Prediction button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button(
        "🔍 Analyze Heart Disease Risk",
        use_container_width=True
    )

if predict_button:
    # Prepare input
    input_data = np.array([[
        age, sex_num, cp_num, trestbps, chol, fbs_num,
        restecg_num, thalach, exang_num, oldpeak,
        slope_num, ca, thal_num
    ]])

    # Make prediction
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    risk_percentage = probability[0][1] * 100

    # Display results
    st.markdown("---")
    st.markdown("### 📊 Analysis Results")

    if prediction[0] == 0:
        st.markdown("""
        <div class="result-card low-risk">
            <h2>✅ Low Risk</h2>
            <p style="font-size: 1.2rem; margin-top: 1rem;">
                The model indicates a <strong>low likelihood</strong>
                of heart disease based on the provided parameters.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card high-risk">
            <h2>⚠️ High Risk</h2>
            <p style="font-size: 1.2rem; margin-top: 1rem;">
                The model indicates a <strong>high likelihood</strong>
                of heart disease. Please consult a healthcare
                professional.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Risk Probability", f"{risk_percentage:.1f}%")
    with col_m2:
        confidence = max(probability[0]) * 100
        st.metric("Confidence", f"{confidence:.1f}%")
    with col_m3:
        risk_level = "High" if prediction[0] == 1 else "Low"
        st.metric("Risk Level", risk_level)

    # Recommendations
    st.markdown("### 💡 Recommendations")
    if prediction[0] == 1:
        st.error("""
        **Immediate Actions:**
        - 🏥 Schedule an appointment with a cardiologist
        - 📋 Get comprehensive cardiac tests
        - 💊 Review current medications with your doctor
        - 🏃‍♂️ Discuss lifestyle modifications
        """)
    else:
        st.success("""
        **Preventive Measures:**
        - 🥗 Maintain a heart-healthy diet
        - 🏃‍♂️ Regular exercise (150 min/week)
        - 🩺 Annual health checkups
        - 🚭 Avoid smoking and excessive alcohol
        """)

    st.info(
        "⚠️ **Medical Disclaimer**: This prediction is based on "
        "statistical models and should not replace professional "
        "medical advice, diagnosis, or treatment."
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>Heart Disease Risk Predictor v1.0</strong></p>
    <p>Powered by Machine Learning | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
