# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

# ------------------ Page Config ------------------
st.set_page_config(page_title="Hume – Human-Centric Manager Demo", layout="wide")
st.markdown("""
<style>
    .main {background-color: #111827; color: white;}
    .block-container {padding-top: 2rem;}
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {color: #93c5fd;}
</style>
""", unsafe_allow_html=True)

# ------------------ Login Screen ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center; height: 80vh; flex-direction: column;'>
        <h1 style='color: #ffffff;'>👥 Hume</h1>
        <h3 style='color: #ccc;'>Human-Centric AI-Powered Manager Assistant</h3>
        <form action='#'>
            <button style='padding: 0.6em 2em; font-size: 1.1rem; background-color: #6366f1; color: white; border: none; border-radius: 5px;' type='submit'>Login</button>
        </form>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Login"):
        with st.spinner("Authenticating Hume Systems..."):
            time.sleep(5)
        st.session_state.logged_in = True
        st.experimental_rerun()
    st.stop()

# ------------------ App Body ------------------
st.title("👥 Hume – Human-Centric Manager Assistant")
st.markdown("---")

# ------------------ Dataset (Optional Display) ------------------
st.subheader("📋 Team Dataset (Optional, for Demo Viewing)")
df = None
try:
    df = pd.read_csv("hume_demo_team_data.csv")
    st.dataframe(df, use_container_width=True)
except:
    st.warning("Dataset not found. You can still try the analysis below by entering new data.")

# ------------------ Team-Wide Charts ------------------
if df is not None:
    st.markdown("---")
    st.subheader("📊 Team-Wide Analytics")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔥 Burnout Risk by Mood")
        mood_map = df["Mood"].str.lower().apply(
            lambda x: "High" if any(word in x for word in ["tired", "overwhelmed", "stressed", "anxious", "worried"]) else "Normal"
        )
        mood_df = pd.DataFrame({"Name": df["Name"], "Burnout Risk": mood_map})
        fig = px.histogram(mood_df, x="Burnout Risk", color="Burnout Risk", title="Burnout Risk Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚔️ Conflict Risk by DISC + Mood")
        df["Conflict Risk"] = df.apply(lambda row:
            "High" if row["DISC"] in ["D", "C"] and any(word in str(row["Mood"]).lower() for word in ["frustrated", "angry", "stuck"]) else "Low",
            axis=1)
        fig2 = px.pie(df, names="Conflict Risk", title="Conflict Risk Potential")
        st.plotly_chart(fig2, use_container_width=True)

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
    explanation = []

    # DISC insights
    if disc == "D":
        insights.append("🧠 Dominant personality – direct, challenge-driven, prefers strategic tasks.")
        explanation.append("D-type prefers to take control and thrives when given leadership opportunities or decision-making power.")
    elif disc == "I":
        insights.append("💬 Influencer – values enthusiasm and team energy. Recognize their ideas.")
        explanation.append("I-type individuals are highly social, respond well to verbal encouragement, and enjoy collaborative recognition.")
    elif disc == "S":
        insights.append("🫶 Steady – values stability and appreciation. Avoid pressure.")
        explanation.append("S-types are reliable but do not enjoy sudden changes or emotional volatility in leadership.")
    elif disc == "C":
        insights.append("📊 Conscientious – prefers structure, data, and well-defined goals.")
        explanation.append("C-types want clarity and logic. Overcommunication and ambiguity may cause frustration.")

    # Motivation insight (McClelland)
    if motivation == "Achievement":
        insights.append("🎯 Achievement-driven – assign goal-oriented, challenging work.")
        explanation.append("This team member thrives on hitting measurable outcomes and goal posts.")
    elif motivation == "Affiliation":
        insights.append("👥 Affiliation-oriented – thrives in collaborative environments.")
        explanation.append("Focus on connection and team integration to improve engagement.")
    elif motivation == "Power":
        insights.append("🧭 Power-driven – values influence and leadership opportunities.")
        explanation.append("Delegate high-ownership tasks and involve in decision-making.")

    # Mood interpretation (Maslow or burnout signal)
    mood_words = mood.lower()
    if any(word in mood_words for word in ["tired", "stressed", "overwhelmed", "anxious"]):
        insights.append("⚠️ Emotional fatigue detected – may need support or recovery time.")
        explanation.append("This may correspond to a lack of safety or belonging (Maslow). Suggest wellness time or empathy-based check-in.")
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
            75 if any(k in goal.lower() for k in ["deploy", "automation", "execute"]) else 50,
            85 if motivation == "Affiliation" else 50,
            70 if "research" in goal.lower() or bigfive == "High Openness" else 50,
            90 if motivation == "Achievement" else 60
        ]
    }
    return insights, chart_data, explanation

# ------------------ Display Results ------------------
if submitted:
    with st.spinner("Analyzing team member profile with HR frameworks and emotional signals..."):
        time.sleep(1.5)
        insights, radar, explanation = analyze_theory(name, disc, bigfive, motivation, mood, perf, goal, manager_mood)

    st.markdown("---")
    st.subheader(f"🔍 AI-Powered Analysis for {name}")

    for i in insights:
        st.markdown(f"- {i}")

    with st.expander("🧠 Why These Insights Were Generated"):
        for e in explanation:
            st.markdown(f"• {e}")

    st.markdown("---")
    st.subheader("📈 Skill Emphasis Radar")
    st.markdown("This radar chart visualizes the **dominant skill themes** inferred from the member's goal, DISC type, and motivation profile. Higher scores indicate stronger alignment or opportunity.")

    fig = px.line_polar(r=radar["values"], theta=radar["labels"], line_close=True, title="Skill Focus Area Based on Goal")
    fig.update_traces(fill='toself')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
