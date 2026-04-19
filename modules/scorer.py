import random  # ✅ ONLY HERE (top of file)

def score_opportunity(row, user_field, user_level, user_location):

    score = 0

    # 🎯 FIELD MATCH
    if row["field"] == user_field:
        score += 30
    else:
        score += 10

    # 📊 LEVEL MATCH
    if row["level"] == user_level:
        score += 25
    else:
        score += 10

    # 🌍 GEO
    geo_level = row.get("geo_level", "Global")

    if user_location == "Benin":
        if geo_level == "Local":
            score += 20
        elif geo_level == "Regional":
            score += 15
        else:
            score += 10
    else:
        score += 10

    # ⚡ ACCESS
    access_score = row.get("access_score", 1)
    score += access_score * 4

    # 🧠 MATCH SCORE
    match_score = row.get("match_score", 0)
    score += match_score * 0.1

    # 🎯 PROVIDER DIFFERENCE
    provider = row.get("provider", "")

    if provider == "Google":
        score += 2
    elif provider == "ALX":
        score -= 2

    # ⚖️ REALISM
    if score > 85:
        score -= 5

    if row["type"] == "Job" and user_level == "Beginner":
        score -= 5

    # 🎲 CONTROLLED VARIATION (FINAL STEP)
    score += 0

    return int(min(max(score, 40), 95))


# -------------------------------
# 🎯 SUCCESS INDICATOR (UPGRADED)
# -------------------------------
def success_indicator(score):
    if score >= 90:
        return "🏆 Exceptional match — very strong candidate"
    elif score >= 75:
        return "🔥 Strong match — high chance of success"
    elif score >= 60:
        return "⚡ Moderate match — competitive but possible"
    elif score >= 50:
        return "⚠️ Low match — requires improvement"
    else:
        return "❌ Weak match — not recommended"


# -------------------------------
# 🏆 ADMISSION PROBABILITY
# -------------------------------
def admission_probability(score):
    if score >= 90:
        return "Very High (85–95%)"
    elif score >= 80:
        return "High (70–85%)"
    elif score >= 70:
        return "Moderate (50–70%)"
    elif score >= 60:
        return "Low–Moderate (30–50%)"
    else:
        return "Low (10–30%)"


# -------------------------------
# 🏆 NARRATIVE GENERATOR (ELITE)
# -------------------------------
def generate_narrative(user_field, user_level, user_location, insights):

    # Clean system noise
    clean_insights = [
        i for i in insights
        if not any(word in i.lower() for word in [
            "opportunity",
            "score",
            "available",
            "found",
            "diverse",
            "accessibility"
        ])
    ]

    insights_text = " ".join(clean_insights)

    narrative = f"""
🏆 Leadership Narrative — COMS Project

📌 Context:
As the developer of the Community Opportunity Mapping System (COMS), I analyzed how access to {user_field} opportunities varies for individuals at the {user_level} level in {user_location}.

📊 Analysis:
The system reveals that opportunity access is shaped by both skill level and geographic constraints. While local availability may vary, regional and global opportunities help expand access beyond national limitations.

🧠 Key Insights:
{insights_text if insights_text else "The analysis indicates mixed availability of opportunities across different regions."}

🌍 Interpretation:
This demonstrates that opportunity inequality is not only a function of skills, but also of geography and accessibility. Digital and remote opportunities play a critical role in bridging this gap.

🚀 Conclusion:
This project reflects my commitment to building data-driven systems that improve access to education and career opportunities for underserved communities.
"""

    return narrative.strip()


# -------------------------------
# ❌ REJECTION RISK ANALYSIS
# -------------------------------
def rejection_risk(score):
    if score >= 80:
        return [
            "High competition from equally qualified candidates",
            "Limited selection capacity despite strong profile"
        ]
    elif score >= 65:
        return [
            "Profile meets criteria but lacks differentiation",
            "Potential gaps in experience or positioning"
        ]
    else:
        return [
            "Insufficient alignment with selection criteria",
            "Significant gaps in readiness or competitiveness"
        ]


# -------------------------------
# 🧠 COMPETITIVENESS LEVEL
# -------------------------------
def competitiveness_level(score):
    if score >= 85:
        return "🏆 Extremely competitive — top-tier candidate pool"
    elif score >= 75:
        return "🔥 Highly competitive — strong applicants expected"
    elif score >= 65:
        return "⚡ Moderately competitive — realistic but challenging"
    elif score >= 50:
        return "⚠️ Competitive — noticeable gaps vs top candidates"
    else:
        return "❌ Low competitiveness — unlikely selection outcome"


# -------------------------------
# 🧠 EVALUATION BREAKDOWN (NEW)
# -------------------------------
def evaluate_components(row, user_field, user_level, user_location):

    breakdown = {}

    # 🎯 FIELD
    if row["field"] == user_field:
        breakdown["field"] = ("strong", 30)
    else:
        breakdown["field"] = ("partial", 10)

    # 📊 LEVEL
    if row["level"] == user_level:
        breakdown["level"] = ("aligned", 25)
    else:
        breakdown["level"] = ("mismatch", 10)

    # 🌍 GEO
    geo_level = row.get("geo_level", "Global")

    if user_location in ["Benin", "Africa"]:
        if geo_level == "Local":
            breakdown["geo"] = ("local advantage", 20)
        elif geo_level == "Regional":
            breakdown["geo"] = ("regional access", 15)
        else:
            breakdown["geo"] = ("global access", 10)
    else:
        breakdown["geo"] = ("general access", 10)

    # ⚡ ACCESS
    access_score = row.get("access_score", 1)
    breakdown["access"] = ("accessibility factor", access_score * 4)

    # 🧠 MATCH
    match_score = row.get("match_score", 0)
    breakdown["match"] = ("profile signal", round(match_score * 0.1, 1))

    # 🎯 PROVIDER
    provider = row.get("provider", "")

    if provider == "Google":
        breakdown["provider"] = ("brand advantage", 2)
    elif provider == "ALX":
        breakdown["provider"] = ("neutral impact", -2)
    else:
        breakdown["provider"] = ("neutral", 0)

    return breakdown