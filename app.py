import pandas as pd

# Create a mock dataset with 10 members for the Hume demo
data = [
    {
        "Name": "Sarah Lee",
        "Role": "Product Designer",
        "DISC": "S",
        "BigFive": "High Agreeableness",
        "Motivation": "Achievement",
        "Mood": "Tired, stuck",
        "PerformanceTrend": "Down",
        "Last1on1": "2025-07-01",
        "Goal": "Move into strategy",
        "ManagerMood": "Frustrated"
    },
    {
        "Name": "James Kim",
        "Role": "Backend Engineer",
        "DISC": "C",
        "BigFive": "High Conscientiousness",
        "Motivation": "Power",
        "Mood": "Focused",
        "PerformanceTrend": "Stable",
        "Last1on1": "2025-07-15",
        "Goal": "Become Tech Lead",
        "ManagerMood": "Calm"
    },
    {
        "Name": "Aisha Patel",
        "Role": "QA Analyst",
        "DISC": "I",
        "BigFive": "High Extraversion",
        "Motivation": "Affiliation",
        "Mood": "Overwhelmed",
        "PerformanceTrend": "Slight Decline",
        "Last1on1": "2025-07-05",
        "Goal": "Improve automation skills",
        "ManagerMood": "Busy"
    },
    {
        "Name": "Daniel Wu",
        "Role": "Frontend Developer",
        "DISC": "D",
        "BigFive": "Low Neuroticism",
        "Motivation": "Achievement",
        "Mood": "Energetic",
        "PerformanceTrend": "Up",
        "Last1on1": "2025-07-20",
        "Goal": "Lead UI redesign",
        "ManagerMood": "Positive"
    },
    {
        "Name": "Maya Singh",
        "Role": "Project Manager",
        "DISC": "C",
        "BigFive": "High Conscientiousness",
        "Motivation": "Power",
        "Mood": "Anxious",
        "PerformanceTrend": "Flat",
        "Last1on1": "2025-06-25",
        "Goal": "Cross-team leadership",
        "ManagerMood": "Neutral"
    },
    {
        "Name": "Leo Garcia",
        "Role": "DevOps Engineer",
        "DISC": "S",
        "BigFive": "Low Extraversion",
        "Motivation": "Affiliation",
        "Mood": "Fine",
        "PerformanceTrend": "Stable",
        "Last1on1": "2025-07-10",
        "Goal": "Infrastructure automation",
        "ManagerMood": "Positive"
    },
    {
        "Name": "Emily Chen",
        "Role": "Data Scientist",
        "DISC": "D",
        "BigFive": "High Openness",
        "Motivation": "Achievement",
        "Mood": "Inspired",
        "PerformanceTrend": "Strong Upward",
        "Last1on1": "2025-07-18",
        "Goal": "Publish internal research",
        "ManagerMood": "Supportive"
    },
    {
        "Name": "Mohamed Hassan",
        "Role": "Security Analyst",
        "DISC": "C",
        "BigFive": "High Conscientiousness",
        "Motivation": "Power",
        "Mood": "Worried",
        "PerformanceTrend": "Drop",
        "Last1on1": "2025-06-30",
        "Goal": "Security team lead",
        "ManagerMood": "Concerned"
    },
    {
        "Name": "Isabella Rossi",
        "Role": "UX Researcher",
        "DISC": "I",
        "BigFive": "High Agreeableness",
        "Motivation": "Affiliation",
        "Mood": "Thoughtful",
        "PerformanceTrend": "Stable",
        "Last1on1": "2025-07-12",
        "Goal": "Improve research visibility",
        "ManagerMood": "Calm"
    },
    {
        "Name": "Ethan Johnson",
        "Role": "AI Engineer",
        "DISC": "D",
        "BigFive": "High Openness",
        "Motivation": "Achievement",
        "Mood": "Stressed",
        "PerformanceTrend": "Volatile",
        "Last1on1": "2025-07-03",
        "Goal": "Deploy ML platform",
        "ManagerMood": "Busy"
    }
]

df = pd.DataFrame(data)
csv_path = "/mnt/data/hume_demo_team_data.csv"
df.to_csv(csv_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Hume Demo Team Dataset", dataframe=df)
csv_path
