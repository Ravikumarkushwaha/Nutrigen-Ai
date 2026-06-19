import streamlit as st
from google import genai
from google.genai import types
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import os

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NutriGen AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  DESIGN SYSTEM  (Dark Forest Theme)
# ─────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:        #0D1A12;
  --surface:   #122019;
  --panel:     #1A2E22;
  --border:    #2A4035;
  --lime:      #BCEF5A;
  --lime-dim:  #8DB845;
  --sage:      #5E8F6E;
  --cream:     #EDE8DA;
  --muted:     #7A9A86;
  --danger:    #E8674A;
  --gold:      #D4A843;
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-body:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
  background-color: var(--bg) !important;
  color: var(--cream) !important;
  font-family: var(--font-body) !important;
}

[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }

.nutrigen-hero {
  text-align: center;
  padding: 2.4rem 1rem 1.6rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 2rem;
}
.nutrigen-hero h1 {
  font-family: var(--font-display) !important;
  font-size: clamp(2.2rem, 5vw, 3.6rem) !important;
  color: var(--lime) !important;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin-bottom: 0.4rem;
}
.nutrigen-hero p {
  color: var(--muted) !important;
  font-size: 1rem;
  font-weight: 300;
  letter-spacing: 0.04em;
}

.section-label {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--lime-dim);
  margin-bottom: 0.6rem;
  display: block;
}

.ng-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1rem;
}
.ng-card p, .ng-card li { color: var(--muted) !important; font-size: 0.93rem; line-height: 1.65; }

.metric-pill {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.65rem 1.1rem;
  margin-bottom: 0.5rem;
}
.metric-pill .val {
  font-family: var(--font-mono);
  font-size: 1.45rem;
  color: var(--lime);
  font-weight: 500;
}
.metric-pill .lbl { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.06em; }

.ai-bubble {
  background: var(--surface);
  border-left: 3px solid var(--lime);
  border-radius: 0 8px 8px 0;
  padding: 1.2rem 1.4rem;
  margin: 1rem 0;
}
.ai-bubble p   { color: var(--cream) !important; margin-bottom: 0.5rem; line-height: 1.7; font-size: 0.94rem; }
.ai-bubble li  { color: var(--cream) !important; margin-bottom: 0.25rem; line-height: 1.65; font-size: 0.93rem; }
.ai-bubble ul, .ai-bubble ol { padding-left: 1.4rem; margin-bottom: 0.5rem; }
.ai-bubble h1, .ai-bubble h2, .ai-bubble h3, .ai-bubble h4 {
  color: var(--lime) !important;
  font-family: var(--font-display) !important;
  margin-top: 1rem; margin-bottom: 0.35rem;
}
.ai-bubble strong { color: var(--cream) !important; font-weight: 600; }
.ai-bubble em { color: var(--muted) !important; }
.ai-bubble table { width: 100%; border-collapse: collapse; margin: 0.75rem 0; font-size: 0.88rem; }
.ai-bubble th { background: var(--panel); color: var(--lime) !important; padding: 0.5rem 0.75rem; border: 1px solid var(--border); text-align: left; }
.ai-bubble td { color: var(--cream) !important; padding: 0.45rem 0.75rem; border: 1px solid var(--border); }
.ai-bubble tr:nth-child(even) td { background: var(--panel); }
.ai-bubble code { background: var(--panel); color: var(--lime) !important; padding: 0.1rem 0.4rem; border-radius: 4px; font-family: var(--font-mono); font-size: 0.85rem; }
.ai-bubble hr { border-color: var(--border) !important; margin: 0.75rem 0; }

.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
  background-color: var(--panel) !important;
  border: 1px solid var(--border) !important;
  color: var(--cream) !important;
  border-radius: 6px !important;
}

/* Button: lime background, dark text, always visible */
.stButton > button {
  background: var(--lime) !important;
  color: #0D1A12 !important;
  border: none !important;
  border-radius: 6px !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.04em !important;
  padding: 0.55rem 1.4rem !important;
  transition: all 0.15s !important;
}
.stButton > button:hover {
  background: var(--lime-dim) !important;
  color: #0D1A12 !important;
  transform: translateY(-1px) !important;
}
.stButton > button p,
.stButton > button span { color: #0D1A12 !important; }

.stSlider > div { color: var(--cream) !important; }

.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  font-size: 0.88rem !important;
  padding: 0.6rem 1.2rem !important;
  border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
  color: var(--lime) !important;
  border-bottom: 2px solid var(--lime) !important;
}

[data-testid="stFileUploader"] {
  background: var(--panel) !important;
  border: 1px dashed var(--border) !important;
  border-radius: 8px !important;
}

.streamlit-expanderHeader {
  background: var(--panel) !important;
  color: var(--cream) !important;
  border-radius: 6px !important;
}

hr { border-color: var(--border) !important; }
#MainMenu, footer { visibility: hidden; }
header { visibility: visible !important; background: transparent !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
def _init():
    # API key: env var (local) → Streamlit secrets (cloud)
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""

    defaults = {
        "profile": {},
        "meal_plan": "",
        "workout_plan": "",
        "food_analysis": "",
        "health_insights": "",
        "budget_recs": "",
        "wellness_log": [],
        "chat_history": [],
        "gemini_key": api_key,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

MODEL = "gemini-3.1-flash-lite"

# ─────────────────────────────────────────────
#  GEMINI HELPERS  (new google-genai SDK)
# ─────────────────────────────────────────────
def get_client() -> genai.Client:
    return genai.Client(api_key=st.session_state["gemini_key"])

def chat_complete(prompt: str, system: str = "",
                  image_bytes: bytes = None, image_mime: str = None) -> str:
    if not st.session_state["gemini_key"]:
        return "⚠️ No Gemini API key found. Set GEMINI_API_KEY in your environment or Streamlit secrets."
    try:
        client = get_client()
        parts = []
        if image_bytes:
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime))
        parts.append(types.Part.from_text(text=prompt))
        cfg = types.GenerateContentConfig(
            max_output_tokens=1800,
            system_instruction=system or None,
        )
        resp = client.models.generate_content(
            model=MODEL,
            contents=parts,
            config=cfg,
        )
        return resp.text
    except Exception as e:
        return f"❌ Error: {e}"

def chat_complete_history(history: list, system: str = "") -> str:
    if not st.session_state["gemini_key"]:
        return "⚠️ No Gemini API key found. Set GEMINI_API_KEY in your environment or Streamlit secrets."
    try:
        client = get_client()
        contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
        cfg = types.GenerateContentConfig(
            max_output_tokens=1200,
            system_instruction=system or None,
        )
        resp = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=cfg,
        )
        return resp.text
    except Exception as e:
        return f"❌ Error: {e}"

def show_ai_response(text: str):
    """Render AI markdown inside a styled bubble."""
    st.markdown('<div class="ai-bubble">', unsafe_allow_html=True)
    st.markdown(text)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PROFILE HELPERS
# ─────────────────────────────────────────────
def profile_summary(p: dict) -> str:
    if not p:
        return "No profile set."
    return (
        f"Name: {p.get('name','User')}, Age: {p.get('age','?')}, "
        f"Gender: {p.get('gender','?')}, Height: {p.get('height','?')} cm, "
        f"Weight: {p.get('weight','?')} kg, Goal: {p.get('goal','?')}, "
        f"Activity: {p.get('activity','?')}, Diet: {p.get('diet','?')}, "
        f"Allergies: {p.get('allergies','None')}, Budget: ₹{p.get('budget','?')}/day"
    )

def bmi(h, w):
    try:
        h_m = float(h) / 100
        return round(float(w) / (h_m ** 2), 1)
    except Exception:
        return None

def bmr(age, gender, h, w):
    try:
        if gender == "Male":
            return round(88.362 + 13.397*float(w) + 4.799*float(h) - 5.677*float(age))
        else:
            return round(447.593 + 9.247*float(w) + 3.098*float(h) - 4.330*float(age))
    except Exception:
        return None

ACTIVITY_MUL = {
    "Sedentary": 1.2, "Lightly Active": 1.375,
    "Moderately Active": 1.55, "Very Active": 1.725, "Extra Active": 1.9,
}

def tdee(age, gender, h, w, activity):
    b = bmr(age, gender, h, w)
    return round(b * ACTIVITY_MUL.get(activity, 1.55)) if b else None

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="section-label">Your Profile</span>', unsafe_allow_html=True)
    p = st.session_state["profile"]

    name = st.text_input("Name", value=p.get("name", ""), placeholder="e.g. Priya")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 10, 100, int(p.get("age", 25)))
        h   = st.number_input("Height (cm)", 100, 250, int(p.get("height", 165)))
    with col2:
        gender = st.selectbox("Gender", ["Female", "Male", "Other"],
                               index=["Female","Male","Other"].index(p.get("gender","Female")))
        w = st.number_input("Weight (kg)", 30, 250, int(p.get("weight", 60)))

    goal = st.selectbox("Goal", [
        "Weight Loss","Muscle Gain","Maintenance","Athletic Performance",
        "Improve Energy","Manage Diabetes","Heart Health"],
        index=["Weight Loss","Muscle Gain","Maintenance","Athletic Performance",
               "Improve Energy","Manage Diabetes","Heart Health"].index(p.get("goal","Maintenance")))

    activity = st.selectbox("Activity Level", list(ACTIVITY_MUL.keys()),
                             index=list(ACTIVITY_MUL.keys()).index(p.get("activity","Moderately Active")))

    diet = st.selectbox("Diet Type", [
        "Omnivore","Vegetarian","Vegan","Keto","Paleo",
        "Mediterranean","Gluten-Free","Diabetic-Friendly"],
        index=["Omnivore","Vegetarian","Vegan","Keto","Paleo",
               "Mediterranean","Gluten-Free","Diabetic-Friendly"].index(p.get("diet","Omnivore")))

    allergies = st.text_input("Allergies / Avoidances", value=p.get("allergies",""),
                               placeholder="e.g. nuts, dairy")
    budget = st.slider("Daily Food Budget (₹)", 50, 1000, int(p.get("budget", 300)), step=50)

    if st.button("💾  Save Profile", use_container_width=True):
        st.session_state["profile"] = {
            "name": name, "age": age, "gender": gender,
            "height": h, "weight": w, "goal": goal,
            "activity": activity, "diet": diet,
            "allergies": allergies, "budget": budget,
        }
        st.success("Profile saved!")

    st.divider()
    b_val = bmi(h, w)
    t_val = tdee(age, gender, h, w, activity)
    if b_val:
        st.markdown(f'<div class="metric-pill"><div class="val">{b_val}</div><div class="lbl">BMI</div></div>', unsafe_allow_html=True)
    if t_val:
        st.markdown(f'<div class="metric-pill"><div class="val">{t_val:,}</div><div class="lbl">TDEE kcal/day</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="nutrigen-hero">
  <h1>🌿 NutriGen AI</h1>
  <p>Intelligent Health, Nutrition &amp; Fitness — powered by Gemini 2.0 Flash</p>
</div>
""", unsafe_allow_html=True)

prof_txt = profile_summary(st.session_state["profile"])
SYS = f"""You are NutriGen AI, an expert nutritionist, fitness trainer, and wellness coach.
Current user profile: {prof_txt}
Be specific, practical, and evidence-based. Format output with clear sections and emoji headers.
Tailor every recommendation to the user's goal, diet type, allergies, and budget."""

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "🥗 Meal Plan",
    "🏋️ Workout",
    "📸 Food Scan",
    "💡 Health Insights",
    "💰 Budget Nutrition",
    "📊 Wellness Tracker",
    "🤖 AI Chat",
])

# ══════════════════════════════════════════════
#  TAB 1 – MEAL PLAN
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown('<span class="section-label">Personalised Meal Plan</span>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        days = st.selectbox("Duration", ["1 day","3 days","7 days"], index=1)
    with col2:
        meals_pd = st.selectbox("Meals per day", ["3 meals","4 meals","5 meals (with snacks)"])
    with col3:
        cuisine = st.selectbox("Cuisine preference", ["Indian","Mediterranean","Pan-Asian","Western","Mixed"])

    special = st.text_input("Special notes", placeholder="e.g. high-protein breakfast, no onion-garlic...")

    if st.button("🌿  Generate Meal Plan", use_container_width=True):
        if not st.session_state["profile"]:
            st.warning("Please fill in your profile in the sidebar first.")
        else:
            prompt = f"""Create a detailed {days} meal plan with {meals_pd} for a {cuisine} cuisine preference.
Special notes: {special or 'None'}.
For each meal include: dish name, key ingredients, approximate calories, macros (P/C/F), prep time, and a brief cooking tip.
End with a daily nutrition summary table and grocery list."""
            with st.spinner("Crafting your meal plan…"):
                result = chat_complete(prompt, SYS)
            st.session_state["meal_plan"] = result

    if st.session_state["meal_plan"]:
        show_ai_response(st.session_state["meal_plan"])
        st.download_button("⬇ Download Meal Plan", st.session_state["meal_plan"], "meal_plan.txt", "text/plain")

# ══════════════════════════════════════════════
#  TAB 2 – WORKOUT
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<span class="section-label">Workout Routine</span>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        wtype = st.selectbox("Workout type", [
            "Full Body","Push/Pull/Legs","Upper/Lower Split",
            "HIIT","Yoga & Mobility","Cardio Focus","Home Workout (no equipment)"])
        wdays = st.selectbox("Days per week", ["3 days","4 days","5 days","6 days"])
    with col2:
        wlevel = st.selectbox("Fitness level", ["Beginner","Intermediate","Advanced"])
        wloc   = st.selectbox("Location", ["Gym","Home","Outdoor","Mixed"])

    injury = st.text_input("Injuries / limitations", placeholder="e.g. lower back pain, knee injury")

    if st.button("🏋️  Generate Workout Plan", use_container_width=True):
        if not st.session_state["profile"]:
            st.warning("Fill in your profile first.")
        else:
            prompt = f"""Design a {wdays} {wtype} workout routine.
Level: {wlevel}, Location: {wloc}, Injuries: {injury or 'None'}.
For each workout day include: warm-up, main exercises (sets × reps, rest), cool-down.
Include exercise descriptions, safety cues, progression notes, and a weekly volume summary.
Also suggest complementary nutrition timing (pre/post workout meals)."""
            with st.spinner("Building your workout…"):
                result = chat_complete(prompt, SYS)
            st.session_state["workout_plan"] = result

    if st.session_state["workout_plan"]:
        show_ai_response(st.session_state["workout_plan"])
        st.download_button("⬇ Download Workout Plan", st.session_state["workout_plan"], "workout_plan.txt", "text/plain")

# ══════════════════════════════════════════════
#  TAB 3 – FOOD SCAN
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<span class="section-label">Food Image Analysis</span>', unsafe_allow_html=True)
    st.markdown('<div class="ng-card"><p>Upload a photo of any meal, ingredient, or food package. Gemini Vision will identify it, estimate nutritional content, and tell you how it fits your goals.</p></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload food image", type=["jpg","jpeg","png","webp"])
    extra_q  = st.text_input("Specific question about this food?", placeholder="e.g. Is this suitable for my diabetes goal?")

    if st.button("📸  Analyse Food", use_container_width=True):
        if not uploaded:
            st.warning("Please upload an image first.")
        else:
            img_bytes = uploaded.read()
            ext  = uploaded.name.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ("jpg","jpeg") else f"image/{ext}"
            prompt_text = f"""Analyse this food image for a user whose profile is: {prof_txt}
1. Identify the dish/ingredients visible
2. Estimate: calories, protein, carbs, fat, fibre, key micronutrients
3. Rate this food for the user's goal ({st.session_state['profile'].get('goal','health')}) out of 10
4. List 3 healthier alternatives or modifications
5. Note any allergen concerns given allergies: {st.session_state['profile'].get('allergies','None')}
{f'6. Answer this specific question: {extra_q}' if extra_q else ''}"""
            with st.spinner("Scanning your food…"):
                result = chat_complete(prompt_text, SYS, image_bytes=img_bytes, image_mime=mime)
            st.session_state["food_analysis"] = result

    col1, col2 = st.columns([1, 2])
    with col1:
        if uploaded:
            st.image(uploaded, caption="Uploaded food", use_container_width=True)
    with col2:
        if st.session_state["food_analysis"]:
            show_ai_response(st.session_state["food_analysis"])

# ══════════════════════════════════════════════
#  TAB 4 – HEALTH INSIGHTS
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<span class="section-label">Personalised Health Insights</span>', unsafe_allow_html=True)

    insight_type = st.selectbox("Insight category", [
        "Overall Health Assessment","Nutritional Deficiency Risk",
        "Hormonal & Metabolic Health","Gut Health & Digestion",
        "Sleep & Recovery Optimisation","Stress & Mental Wellness",
        "Cardiovascular Health","Bone & Joint Health",
    ])
    symptoms = st.text_area("Current symptoms or concerns (optional)",
                             placeholder="e.g. fatigue, bloating, poor sleep, brain fog…", height=80)
    labs     = st.text_area("Recent lab results (optional)",
                             placeholder="e.g. Hb: 10.5, Vitamin D: 18 ng/mL, TSH: 3.2…", height=80)

    if st.button("💡  Generate Health Insights", use_container_width=True):
        if not st.session_state["profile"]:
            st.warning("Fill in your profile first.")
        else:
            prompt = f"""Provide a detailed {insight_type} for this user.
Symptoms: {symptoms or 'None reported'}.
Lab values: {labs or 'None provided'}.
Give:
1. Current risk assessment based on their profile
2. Root-cause analysis of any symptoms
3. Top 5 evidence-based nutrition/lifestyle interventions
4. Foods to prioritise and avoid
5. Supplement recommendations (with dosages) if applicable
6. When to seek professional medical care
Note: This is educational content, not a medical diagnosis."""
            with st.spinner("Analysing health data…"):
                result = chat_complete(prompt, SYS)
            st.session_state["health_insights"] = result

    if st.session_state["health_insights"]:
        show_ai_response(st.session_state["health_insights"])

    if st.session_state["profile"]:
        st.divider()
        st.markdown('<span class="section-label">Your Body Metrics</span>', unsafe_allow_html=True)
        p2    = st.session_state["profile"]
        b_val = bmi(p2["height"], p2["weight"])
        t_val = tdee(p2["age"], p2["gender"], p2["height"], p2["weight"], p2["activity"])

        if b_val and t_val:
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=b_val,
                    title={"text": "BMI", "font": {"color": "#EDE8DA", "family": "Inter"}},
                    number={"font": {"color": "#BCEF5A"}},
                    gauge={
                        "axis": {"range": [10, 45], "tickcolor": "#5E8F6E"},
                        "bar": {"color": "#BCEF5A"},
                        "bgcolor": "#1A2E22",
                        "steps": [
                            {"range": [10, 18.5], "color": "#3A6A8A"},
                            {"range": [18.5, 25], "color": "#2A5E3A"},
                            {"range": [25, 30],   "color": "#8A6A2A"},
                            {"range": [30, 45],   "color": "#7A3A2A"},
                        ],
                    },
                ))
                fig.update_layout(paper_bgcolor="#0D1A12", font_color="#EDE8DA",
                                  height=240, margin=dict(l=20,r=20,t=40,b=20))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                goal_map = {
                    "Weight Loss": (35,35,30), "Muscle Gain": (40,35,25),
                    "Maintenance": (30,40,30), "Athletic Performance": (35,45,20),
                    "Improve Energy": (25,50,25), "Manage Diabetes": (30,30,40),
                    "Heart Health": (25,45,30),
                }
                pro, carb, fat = goal_map.get(p2["goal"], (30,40,30))
                fig2 = go.Figure(go.Pie(
                    labels=["Protein","Carbs","Fat"], values=[pro, carb, fat],
                    hole=0.55, marker_colors=["#BCEF5A","#5E8F6E","#D4A843"],
                    textfont_color="#0D1A12",
                ))
                fig2.update_layout(
                    title={"text": f"Macro Split for {p2['goal']}", "font": {"color": "#EDE8DA"}},
                    paper_bgcolor="#0D1A12", font_color="#EDE8DA",
                    height=240, margin=dict(l=20,r=20,t=40,b=20),
                    legend=dict(font=dict(color="#EDE8DA")),
                )
                st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 5 – BUDGET NUTRITION
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<span class="section-label">Budget-Friendly Nutrition</span>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        bdg  = st.slider("Daily budget (₹)", 50, 800, int(st.session_state["profile"].get("budget", 200)), step=25)
        city = st.text_input("Your city / region", placeholder="e.g. Mumbai, Delhi, Bangalore")
    with col2:
        season = st.selectbox("Current season", ["Summer","Monsoon","Winter","Spring"])
        store  = st.selectbox("Primary shopping at", ["Local market / mandi","Supermarket","Online grocery","Mixed"])

    if st.button("💰  Generate Budget Meal Strategy", use_container_width=True):
        if not st.session_state["profile"]:
            st.warning("Fill in your profile first.")
        else:
            prompt = f"""Create a budget nutrition plan for ₹{bdg}/day in {city or 'India'} ({season} season, shopping at {store}).
Include:
1. Cheapest high-protein foods available locally with price estimates
2. 3-day budget meal plan staying under ₹{bdg}/day total
3. Smart bulk-buying recommendations
4. Cheap seasonal vegetables & fruits to prioritise
5. Low-cost protein sources (dal, eggs, tofu, etc.) with serving suggestions
6. Cost-per-gram-of-protein comparison table
7. Meal-prep strategies to reduce waste and save money
Tailor strictly to user's diet type: {st.session_state['profile'].get('diet','Omnivore')} and goal: {st.session_state['profile'].get('goal','Maintenance')}"""
            with st.spinner("Finding budget-smart foods…"):
                result = chat_complete(prompt, SYS)
            st.session_state["budget_recs"] = result

    if st.session_state["budget_recs"]:
        show_ai_response(st.session_state["budget_recs"])

# ══════════════════════════════════════════════
#  TAB 6 – WELLNESS TRACKER
# ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<span class="section-label">Daily Wellness Log</span>', unsafe_allow_html=True)

    with st.expander("➕  Log Today's Data", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            log_date  = st.date_input("Date", value=datetime.today())
            log_cal   = st.number_input("Calories eaten", 0, 5000, 1800)
            log_water = st.slider("Water (glasses)", 0, 20, 8)
        with col2:
            log_sleep  = st.slider("Sleep (hours)", 0.0, 12.0, 7.5, 0.5)
            log_stress = st.slider("Stress level (1–10)", 1, 10, 4)
            log_energy = st.slider("Energy level (1–10)", 1, 10, 7)
        with col3:
            log_workout = st.checkbox("Worked out today?")
            log_w_dur   = st.number_input("Workout duration (min)", 0, 300, 45) if log_workout else 0
            log_mood    = st.selectbox("Mood", ["😄 Great","🙂 Good","😐 Neutral","😔 Low","😤 Stressed"])
            log_weight_today = st.number_input("Weight today (kg, optional)", 0.0, 300.0, 0.0)

        if st.button("📝  Save Today's Log", use_container_width=True):
            entry = {
                "date": str(log_date), "calories": log_cal, "water": log_water,
                "sleep": log_sleep, "stress": log_stress, "energy": log_energy,
                "workout": log_workout, "workout_min": log_w_dur,
                "mood": log_mood, "weight": log_weight_today,
            }
            st.session_state["wellness_log"] = [
                e for e in st.session_state["wellness_log"] if e["date"] != str(log_date)
            ]
            st.session_state["wellness_log"].append(entry)
            st.session_state["wellness_log"].sort(key=lambda x: x["date"])
            st.success(f"Logged {log_date} ✓")

    log = st.session_state["wellness_log"]
    if log:
        df = pd.DataFrame(log)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        df14 = df.tail(14)

        st.markdown('<span class="section-label">Trends (last 14 days)</span>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(df14, x="date", y="calories", title="Calorie Intake",
                          color_discrete_sequence=["#BCEF5A"])
            fig.update_layout(paper_bgcolor="#0D1A12", plot_bgcolor="#1A2E22",
                              font_color="#EDE8DA", height=220, margin=dict(l=10,r=10,t=35,b=10))
            fig.update_xaxes(gridcolor="#2A4035")
            fig.update_yaxes(gridcolor="#2A4035")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig2 = px.line(df14, x="date", y=["sleep","energy","stress"],
                           title="Sleep / Energy / Stress",
                           color_discrete_sequence=["#5E8F6E","#BCEF5A","#E8674A"])
            fig2.update_layout(paper_bgcolor="#0D1A12", plot_bgcolor="#1A2E22",
                               font_color="#EDE8DA", height=220, margin=dict(l=10,r=10,t=35,b=10),
                               legend=dict(font=dict(color="#EDE8DA")))
            fig2.update_xaxes(gridcolor="#2A4035")
            fig2.update_yaxes(gridcolor="#2A4035")
            st.plotly_chart(fig2, use_container_width=True)

        if df14["weight"].max() > 0:
            fig3 = px.line(df14[df14["weight"] > 0], x="date", y="weight",
                           title="Weight Trend", color_discrete_sequence=["#D4A843"])
            fig3.update_layout(paper_bgcolor="#0D1A12", plot_bgcolor="#1A2E22",
                               font_color="#EDE8DA", height=200, margin=dict(l=10,r=10,t=35,b=10))
            fig3.update_xaxes(gridcolor="#2A4035")
            fig3.update_yaxes(gridcolor="#2A4035")
            st.plotly_chart(fig3, use_container_width=True)

        if len(df14) >= 3 and st.button("🔍  AI Weekly Review", use_container_width=True):
            summary = df14.to_dict(orient="records")
            prompt = f"""Analyse this wellness log data for the past {len(df14)} days:
{json.dumps(summary, default=str, indent=2)}
Provide:
1. Overall wellness score (0–100) with breakdown
2. Key patterns noticed (positive & negative)
3. Top 3 actionable improvements for next week
4. Correlation insights (e.g. sleep vs energy)
5. Progress toward goal: {st.session_state['profile'].get('goal','health')}"""
            with st.spinner("Reviewing your week…"):
                result = chat_complete(prompt, SYS)
            show_ai_response(result)
    else:
        st.markdown('<div class="ng-card"><p>No logs yet. Start logging your daily data above to see trends and AI insights.</p></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 7 – AI CHAT
# ══════════════════════════════════════════════
with tabs[6]:
    st.markdown('<span class="section-label">Ask NutriGen AI Anything</span>', unsafe_allow_html=True)

    st.markdown("**Quick prompts:**")
    qcols = st.columns(4)
    quick = [
        "What should I eat after a workout?",
        "Suggest a high-protein vegetarian breakfast",
        "How can I reduce sugar cravings?",
        "Is intermittent fasting right for me?",
    ]
    for i, q in enumerate(quick):
        with qcols[i]:
            if st.button(q, key=f"qp_{i}", use_container_width=True):
                st.session_state["chat_history"].append({"role": "user", "content": q})
                with st.spinner("Thinking…"):
                    answer = chat_complete_history(st.session_state["chat_history"], SYS)
                st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                st.rerun()

    st.divider()

    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:0.5rem;">
              <div style="background:#2A4035;border-radius:12px 12px 2px 12px;padding:0.7rem 1rem;max-width:75%;font-size:0.9rem;color:#EDE8DA;">
                {msg['content']}
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:0.75rem;">
              <div style="background:#1A2E22;border:1px solid #2A4035;border-radius:12px 12px 12px 2px;padding:0.7rem 1rem;max-width:80%;font-size:0.9rem;color:#EDE8DA;white-space:pre-wrap;">
                🌿 {msg['content']}
              </div>
            </div>""", unsafe_allow_html=True)

    user_input = st.chat_input("Ask about nutrition, fitness, recipes, supplements…")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.spinner("NutriGen AI is thinking…"):
            answer = chat_complete_history(st.session_state["chat_history"], SYS)
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state["chat_history"]:
        if st.button("🗑  Clear Chat", use_container_width=False):
            st.session_state["chat_history"] = []
            st.rerun()