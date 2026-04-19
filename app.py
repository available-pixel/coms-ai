# app.py
import pandas as pd
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from modules.data_loader import load_data
from modules.matcher import match_opportunities
from modules.map_view import render_map
from modules.analyzer import analyze_gaps
from modules.explainer import explain_recommendation
from modules.report import generate_report
from modules.scorer import (
    score_opportunity,
    success_indicator,
    admission_probability,
    generate_narrative,
    rejection_risk,
    competitiveness_level
)

# -------------------------------
# 🎨 PAGE CONFIG (UI UPGRADE)
# -------------------------------
st.set_page_config(
    page_title="COMS AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 🎨 CUSTOM UI (SAFE)
# -------------------------------
st.markdown("""
<style>

/* 🌐 App background */
.stApp {
    background-color: #EAF3FF;
    color: #0B1F3A;
}

/* 🧠 Text styling */
h1, h2, h3, h4, p, span {
    color: #0B1F3A !important;
}

/* 📦 Cards / containers */
div[data-testid="stMarkdownContainer"] > div {
    background-color: #FFFFFF;
    border: 1px solid #CFE3FF;
    border-radius: 14px;
    padding: 10px;
}

/* 🔘 Buttons */
.stButton > button {
    background-color: #4DA3FF;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background-color: #2E8BFF;
    color: white;
}

/* 📊 Metrics */
[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #CFE3FF;
    padding: 10px;
    border-radius: 12px;
}

/* 📂 Sidebar */
section[data-testid="stSidebar"] {
    background-color: #DDEEFF;
}

/* 📏 Divider */
hr {
    border-color: #CFE3FF;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 STATE INITIALIZATION
# -------------------------------
def init_state():
    defaults = {
        "searched": False,
        "local": None,
        "global_": None,
        "insights": [],
        "field": None,
        "level": None,
        "location": None
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# -------------------------------
# 🏠 HERO SECTION (NEW UX)
# -------------------------------
st.markdown("""
<div style="text-align:center;">
    <h1>🌍 Community Opportunity Mapping System</h1>
    <h3>AI-powered opportunity intelligence for students & professionals</h3>
</div>

---
""", unsafe_allow_html=True)

# -------------------------------
# 📊 LOAD DATA
# -------------------------------
df = load_data()

# -------------------------------
# 🎯 SIDEBAR (IMPROVED UX)
# -------------------------------
st.sidebar.title("🎯 Your Profile")

field = st.sidebar.selectbox("Field", ["Tech", "Business", "Social", "Policy"])
level = st.sidebar.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
location = st.sidebar.selectbox("Location", ["Benin", "Africa", "Global", "Remote"])

st.sidebar.markdown("---")
st.sidebar.info("COMS AI matches you with the best opportunities using AI scoring.")

# -------------------------------
# 🚀 SEARCH BUTTON
# -------------------------------
if st.button("🚀 Find Opportunities"):
    local, global_ = match_opportunities(df, field, level, location)

    st.session_state.local = local
    st.session_state.global_ = global_
    st.session_state.field = field
    st.session_state.level = level
    st.session_state.location = location
    st.session_state.searched = True

st.markdown("""
<style>
div.stButton > button {
    background-color: #4DA3FF;
    color: white;
    padding: 0.8rem 1.5rem;
    font-size: 20px;
    border-radius: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🛠 SAFE FUNCTIONS (UNCHANGED)
# -------------------------------
def safe_df(df):
    if df is None:
        return None
    return df.copy()

def process(df):
    if df is None or df.empty:
        return df

    df = df.copy()

    df["score"] = df.apply(
        lambda row: score_opportunity(
            row,
            st.session_state.field,
            st.session_state.level,
            st.session_state.location
        ),
        axis=1
    )

    return df.sort_values("score", ascending=False)

def compute_confidence(top_score, second_score):
    gap = top_score - second_score

    if gap >= 6:
        return "HIGH_CONFIDENCE"
    elif gap >= 3:
        return "MEDIUM_CONFIDENCE"
    else:
        return "LOW_CONFIDENCE"

# -------------------------------
# 📊 DASHBOARD
# -------------------------------
if st.session_state.searched:

    st.success("Analysis completed successfully ✅")

    # -------------------------------
    # 📊 METRICS ROW (NEW UX)
    # -------------------------------
    local_tmp = process(safe_df(st.session_state.local))
    global_tmp = process(safe_df(st.session_state.global_))

    combined_tmp = []
    if local_tmp is not None:
        combined_tmp.append(local_tmp)
    if global_tmp is not None:
        combined_tmp.append(global_tmp)

    if len(combined_tmp) > 0:
        all_tmp = pd.concat(combined_tmp, ignore_index=True)
        top_tmp = all_tmp.sort_values("score", ascending=False).iloc[0]
    else:
        top_tmp = None

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Field", field)
    col2.metric("Level", level)
    col3.metric("Location", location)
    col4.metric("Top Score", int(top_tmp["score"]) if top_tmp is not None else 0)

    st.divider()

    # -------------------------------
    # 🧠 FINAL DATASET
    # -------------------------------
    local = process(safe_df(st.session_state.local))
    global_ = process(safe_df(st.session_state.global_))

    combined = []

    if local is not None and not local.empty:
        combined.append(local)

    if global_ is not None and not global_.empty:
        combined.append(global_)

    if len(combined) == 0:
        st.warning("No opportunities found")
        st.stop()

    all_ops = pd.concat(combined, ignore_index=True)
    all_ops = all_ops.sort_values("score", ascending=False)

    top_op = all_ops.iloc[0]
    second_best = all_ops.iloc[1] if len(all_ops) > 1 else None

    # -------------------------------
    # 🏆 TOP OPPORTUNITY CARD (NEW UI)
    # -------------------------------
    st.markdown("## 🏆 Top Recommendation")

    st.markdown(f"""
    <div style="
        background-color:#EAF3FF;
        padding:20px;
        border-radius:15px;
        border:1px solid #CFE3FF;
        box-shadow: 0px 4px 12px rgba(77, 163, 255, 0.15);
    ">
        <h2 style="color:#0B1F3A;">⭐ {top_op['title']}</h2>
        <p style="color:#0B1F3A;"><b>Score:</b> {top_op['score']}/100</p>
        <p style="color:#4DA3FF;">🚀 Primary AI Recommendation</p>
    </div>
    """, unsafe_allow_html=True)

    st.success(success_indicator(top_op["score"]))
    st.warning(competitiveness_level(top_op["score"]))

    with st.expander("📖 Detailed Explanation"):
        st.write(explain_recommendation(
            top_op,
            st.session_state.field,
            st.session_state.level
        ))

    # -------------------------------
    # 🧠 COMMITTEE ANALYSIS
    # -------------------------------
    if second_best is not None:

        confidence = compute_confidence(top_op["score"], second_best["score"])
        gap = top_op["score"] - second_best["score"]

        st.markdown("## 🧠 Committee Evaluation")

        st.write(f"""
- Comparison: {top_op['title']} vs {second_best['title']}
- Score gap: {gap}
- Confidence: **{confidence.replace('_', ' ').title()}**
        """)

        st.markdown("### 📉 Why alternative was not selected")

        st.write(f"""
{second_best['title']} was not selected due to slightly lower ranking score and weaker alignment in evaluation metrics.
        """)

        st.markdown("### ❌ Risk Analysis")

        for r in rejection_risk(top_op["score"]):
            st.write(f"- {r}")

    st.divider()

    # -------------------------------
    # 📍 LOCAL OPPORTUNITIES (CARDS UI)
    # -------------------------------
    st.subheader("📍 Local Opportunities")

    if local is not None and not local.empty:
        for _, row in local.iterrows():

            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:12px;
                border:1px solid #2C2C2C;
                margin-bottom:10px;
            ">
                <h4>📌 {row['title']}</h4>
                <p>⭐ Score: {row.get('score', 0)}/100</p>
            </div>
            """, unsafe_allow_html=True)

            st.write(explain_recommendation(
                row, st.session_state.field, st.session_state.level
            ))

            st.write(success_indicator(row["score"]))
            st.markdown("---")

        render_map(local, st.session_state.location)

    else:
        st.warning("No local opportunities found")

    # -------------------------------
    # 🌍 GLOBAL OPPORTUNITIES
    # -------------------------------
    st.subheader("🌍 Global Opportunities")

    if global_ is not None and not global_.empty:
        for _, row in global_.iterrows():

            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:12px;
                border:1px solid #2C2C2C;
                margin-bottom:10px;
            ">
                <h4>🌍 {row['title']}</h4>
                <p>⭐ Score: {row.get('score', 0)}/100</p>
            </div>
            """, unsafe_allow_html=True)

            st.write(explain_recommendation(
                row, st.session_state.field, st.session_state.level
            ))

            st.write(success_indicator(row["score"]))
            st.markdown("---")

        render_map(global_, "Global")

    else:
        st.warning("No global opportunities found")

    st.divider()

    # -------------------------------
    # 📊 INSIGHTS
    # -------------------------------
    st.subheader("📊 Community Insights")

    insights = analyze_gaps(local, global_, field, location)
    st.session_state.insights = insights

    for insight in insights:
        st.write(insight)

    st.divider()

    # -------------------------------
    # 📄 ACTIONS PANEL (REPORT SYSTEM)
    # -------------------------------
    st.markdown("## 📄 Actions Panel")

    st.markdown("""
    <div style="
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #CFE3FF;
        background-color: #F7FBFF;
        margin-bottom: 15px;
    ">
        <p style="font-size:16px; margin-bottom:10px;">
            Generate a full AI impact report based on your analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # small spacing hack

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("📄 Generate Impact Report"):

            pdf_buffer = generate_report(
                st.session_state.field,
                st.session_state.level,
                st.session_state.location,
                insights
            )

            st.session_state["pdf_report"] = pdf_buffer

        
    # -------------------------------
    # 👁️ REPORT PREVIEW + DOWNLOAD
    # -------------------------------
    if "pdf_report" in st.session_state:

        st.success("Report ready ✅")

        pdf_viewer(st.session_state["pdf_report"].getvalue())

        st.download_button(
            label="⬇️ Download Impact Report",
            data=st.session_state["pdf_report"],
            file_name="impact_report.pdf",
            mime="application/pdf"
        )

    st.divider()

    # -------------------------------
    # 🏆 NARRATIVE
    # -------------------------------
    st.subheader("🏆 Leadership Narrative")

    narrative = generate_narrative(
        st.session_state.field,
        st.session_state.level,
        st.session_state.location,
        insights
    )

    st.info(narrative)