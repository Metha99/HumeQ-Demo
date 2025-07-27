# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ------------------ Page Config ------------------
st.set_page_config(page_title="Hume – Human-Centric Manager Demo", layout="wide")
st.title("👥 Hume – Human-Centric Manager Assistant")
st.markdown("---")

# ------------------ Dataset (Demo) ------------------
st.subheader("📋 Team Dataset (Optional, for Demo Viewing)")
try:
    df = pd.read_csv("hume_demo_team_data.csv")
    st.dataframe(df, use_container_width=True)
except:
    st.warning("Dataset not found. You can still try the analysis below by entering new data.")

# ------------------ Add New Member Section ------------------
st.markdown("---")
st.subheader("➕ Analyze a New Team Member")

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
        mood = st.text_input("Recent Mood Word(s)")
        perf = st.selectbox("Performance Trend", ["Up", "Stable", "Flat", "Down", "Drop", "Strong Upward", "Volatile"])

    with col3:
        last_1on1 = st.date_input("Last 1-on-1 Date")
        goal = st.text_input("Development Goal")
        manager_mood = st.selectbox("Your Mood Before Interaction", ["Calm", "Positive", "Neutral", "Busy", "Frustrated"])

    submitted = st.form_submit_button("Analyze Team Member")

# ------------------ Analysis Logic ------------------
def analyze_theory(name, disc, bigfive, motivation, mood, perf, goal, manager_mood):
    insights = []
    chart_data = {}

    # DISC insights
    if disc == "D":
        insights.append("🧠 Dominant personality – direct, challenge-driven, prefers strategic tasks.")
    elif disc == "I":
        insights.append("💬 Influencer – values enthusiasm and team energy. Recognize their ideas.")
    elif disc == "S":
        insights.append("🫶 Steady – values stability and appreciation. Avoid pressure.")
    elif disc == "C":
        insights.append("📊 Conscientious – prefers structure, data, and well-defined goals.")

    # Motivation insight (McClelland)
    if motivation == "Achievement":
        insights.append("🎯 Achievement-driven – assign goal-oriented, challenging work.")
    elif motivation == "Affiliation":
        insights.append("👥 Affiliation-oriented – thrives in collaborative environments.")
    elif motivation == "Power":
        insights.append("🧭 Power-driven – values influence and leadership opportunities.")

    # Mood interpretation (Maslow or burnout signal)
    mood_words = mood.lower()
    if any(word in mood_words for word in ["tired", "stressed", "overwhelmed", "anxious"]):
        insights.append("⚠️ Emotional fatigue detected – may need support or recovery time.")
    elif "inspired" in mood_words:
        insights.append("✨ Inspired – great time to assign vision-building tasks.")
    elif "thoughtful" in mood_words:
        insights.append("🧘 Reflective mood – check if they need quiet time or are blocked.")

    # Manager readiness
    if manager_mood.lower() in ["frustrated", "busy"]:
        insights.append("🛑 You may want to pause – your current mood may impact the conversation.")
    else:
        insights.append("✅ You are emotionally ready to engage constructively.")

    # Skill mapping visualization (Goal Radar)
    chart_data = {
        "labels": ["Strategy", "Execution", "Teamwork", "Creativity", "Growth"],
        "values": [
            80 if "strategy" in goal.lower() else 40,
            75 if "deploy" in goal.lower() or "automation" in goal.lower() else 50,
            85 if motivation == "Affiliation" else 50,
            70 if "research" in goal.lower() or bigfive == "High Openness" else 50,
            90 if motivation == "Achievement" else 60
        ]
    }
    return insights, chart_data

# ------------------ Display Results ------------------
if submitted:
    insights, radar = analyze_theory(name, disc, bigfive, motivation, mood, perf, goal, manager_mood)

    st.markdown("---")
    st.subheader(f"🔍 AI-Powered Analysis for {name}")

    for i in insights:
        st.markdown(f"- {i}")

    st.markdown("\n")
    st.subheader("📈 Skill Emphasis Radar")
    fig = px.line_polar(r=radar["values"], theta=radar["labels"], line_close=True, title="Skill Focus Area Based on Goal")
    st.plotly_chart(fig, use_container_width=True)
