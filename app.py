# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
from transformers import pipeline

# ------------------ Page Config ------------------
st.set_page_config(page_title="Hume – Human-Centric Manager Demo", layout="wide")
st.markdown("""
<style>
    body, .main, .block-container {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    .stButton > button {
        background-color: #6366f1;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #1e293b;
        color: white;
    }
    .form-container {
        background-color: #1f2937;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #374151;
        margin-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        color: #c7d2fe;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Login Screen ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
        <style>
            .login-box {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 80vh;
                text-align: center;
            }
        </style>
        <div class="login-box">
            <h1 style="color: #ffffff;">👥 Hume</h1>
            <h3 style="color: #ccc;">Human-Centric AI-Powered Manager Assistant</h3>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Login", key="real_login_button"):
        with st.spinner("Authenticating Hume Systems..."):
            time.sleep(3)
        st.session_state.logged_in = True
        st.rerun()

    st.stop()

# ------------------ Sidebar Navigation ------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🧠 Analyze Member", "📈 Insights"])

# ------------------ Load Dataset ------------------
df = None
try:
    df = pd.read_csv("hume_demo_team_data.csv")
    df = df.drop(columns=["ManagerMood"], errors="ignore")
except:
    df = None

# ------------------ Load HuggingFace Model ------------------
@st.cache_resource
def load_hf_sentiment():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@st.cache_resource
def load_hf_emotion():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

sentiment_clf = load_hf_sentiment()
emotion_clf = load_hf_emotion()

# ------------------ HR Emotion Mapping ------------------
def map_emotion_to_hr_signal(label):
    label = label.lower()
    if label in ["joy", "excitement", "optimism"]:
        return (
            "🎯 This team member appears highly engaged and positively oriented toward work. Consider reinforcing with recognition or new challenges.",
            "McClelland's Theory of Needs (Achievement), Herzberg’s Motivation Factors"
        )
    elif label in ["anger", "disgust"]:
        return (
            "⚠️ Frustration signals detected. There may be blockers, misalignment, or interpersonal tension. Suggest a coaching-style 1-on-1.",
            "Herzberg’s Hygiene Factors, Maslow’s Safety Needs"
        )
    elif label in ["fear", "sadness"]:
        return (
            "🧘 Emotional withdrawal or burnout signs detected. Prioritize emotional safety and check for unmet psychological needs.",
            "Maslow’s Hierarchy of Needs (Safety & Belonging), Herzberg’s Hygiene Factors"
        )
    elif label in ["confusion", "surprise"]:
        return (
            "❓ Potential for misalignment or unclear expectations. Clarify direction or restructure goals.",
            "Tuckman’s Group Development (Storming Phase), Situational Leadership"
        )
    else:
        return (
            "ℹ️ Unable to clearly classify emotion. Default to open-ended check-in.",
            "General Psychological Safety Principle"
        )

# ------------------ Analyze Page ------------------
elif page == "🧠 Analyze Member":
    st.title("🧠 Analyze a New Team Member")
    st.markdown("""<div class='form-container'>""", unsafe_allow_html=True)

    with st.form("member_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input("Full Name")
            role = st.text_input("Role")
            disc = st.selectbox("DISC Type", ["D", "I", "S", "C"])
            motivation = st.selectbox("Motivation Type", ["Achievement", "Affiliation", "Power"])

        with col2:
            bigfive = st.selectbox("Big Five Trait", [
                "High Agreeableness", "High Openness", "Low Neuroticism", 
                "High Conscientiousness", "High Extraversion", "Low Extraversion"])
            mood = st.text_area("Recent Mood or Comment")
            perf = st.selectbox("Performance Trend", ["Up", "Stable", "Flat", "Down", "Drop", "Strong Upward", "Volatile"])

        with col3:
            last_1on1 = st.date_input("Last 1-on-1 Date")
            goal = st.text_input("Development Goal")
            manager_mood = st.selectbox("Your Mood Before Interaction", ["Calm", "Positive", "Neutral", "Busy", "Frustrated"])

        submitted = st.form_submit_button("Analyze Team Member")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        st.markdown("---")
        st.subheader(f"🔍 AI-Powered Analysis for {name}")

        sentiment_result = sentiment_clf(mood)[0]
        emotion_result = emotion_clf(mood)

        if isinstance(emotion_result, list) and isinstance(emotion_result[0], list):
            emotion_result = emotion_result[0][0]
        else:
            emotion_result = emotion_result[0]

        emotion_label = emotion_result['label']
        emotion_score = round(emotion_result['score'] * 100)

        st.markdown(f"**🤖 Sentiment:** {sentiment_result['label']} ({round(sentiment_result['score']*100)}%)")
        st.markdown(f"**🧠 Primary Emotion:** {emotion_label.capitalize()} ({emotion_score}%)")

        hr_insight, theory_used = map_emotion_to_hr_signal(emotion_label)

        st.markdown("---")
        st.markdown("**📌 HR Interpretation:**")
        st.info(hr_insight)

        st.markdown("**📚 Theoretical Basis Used:**")
        st.success(theory_used)

        st.markdown("---")
        st.markdown("_This insight is powered by a small transformer-based AI model hosted locally using HuggingFace._")
