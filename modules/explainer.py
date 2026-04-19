from modules.scorer import evaluate_components

def explain_recommendation(row, user_field, user_level):

    title = row.get("title", "Opportunity")
    provider = row.get("provider", "Unknown provider")
    score = int(row.get("score", 0))

    # 🧠 GET REAL EVALUATION SIGNALS
    breakdown = evaluate_components(row, user_field, user_level, None)

    field_label, field_score = breakdown["field"]
    level_label, level_score = breakdown["level"]
    geo_label, geo_score = breakdown["geo"]
    access_label, access_score = breakdown["access"]
    match_label, match_score = breakdown["match"]
    provider_label, provider_score = breakdown["provider"]

    # -------------------------------
    # 🎯 FIELD (DETERMINISTIC)
    # -------------------------------
    if field_score >= 25:
        field_reason = "demonstrates strong alignment with your selected field"
    else:
        field_reason = "shows partial alignment with your field, requiring adaptation"

    # -------------------------------
    # 📊 LEVEL
    # -------------------------------
    if level_score >= 20:
        level_reason = "closely matches your current level of readiness"
    else:
        level_reason = "introduces a level gap that may require additional preparation"

    # -------------------------------
    # 🌍 GEO (FIXED — LABEL-BASED)
    # -------------------------------

    geo_reason_map = {
        "local advantage": "strongly anchored within your immediate geographic environment",
        "regional access": "accessible across your regional ecosystem",
        "global access": "available internationally",
        "general access": "available across different regions"
    }

    geo_reason = geo_reason_map.get(
        geo_label,
        "geographic scope is flexible but not strongly localized"
    )

    # -------------------------------
    # ⚡ ACCESS
    # -------------------------------
    if access_score >= 8:
        access_reason = "provides high accessibility and flexible participation conditions"
    elif access_score >= 4:
        access_reason = "presents moderate accessibility with some constraints"
    else:
        access_reason = "introduces accessibility limitations that may affect participation"

    # -------------------------------
    # 🎯 SCORE INTERPRETATION
    # -------------------------------
    if score >= 85:
        score_reason = "Evaluation indicates strong alignment across all major criteria, placing this opportunity at the top of the selection pool."
    elif score >= 70:
        score_reason = "Evaluation shows a solid overall fit, with minor gaps that do not significantly reduce viability."
    elif score >= 60:
        score_reason = "Evaluation reflects moderate alignment, with noticeable gaps across one or more criteria."
    else:
        score_reason = "Evaluation reveals limited alignment with key selection criteria."

    # -------------------------------
    # ⚖️ SYNTHESIS (NO RANDOM)
    # -------------------------------
    total_positive = sum([
        field_score >= 25,
        level_score >= 20,
        geo_score >= 15,
        access_score >= 6
    ])

    if total_positive >= 3:
        synthesis = "From an evaluator’s perspective, this opportunity represents a strong and competitive option within the current pool."
    elif total_positive == 2:
        synthesis = "From an evaluator’s perspective, this opportunity is viable but requires strategic positioning."
    else:
        synthesis = "From an evaluator’s perspective, this opportunity presents notable limitations relative to stronger alternatives."

    # -------------------------------
    # 🧾 FINAL OUTPUT
    # -------------------------------
    explanation = f"""
🎯 EVALUATOR ANALYSIS

📌 Evidence Review:
- Field alignment: {field_reason} (+{field_score})
- Level assessment: {level_reason} (+{level_score})
- Geographic scope: {geo_reason} (+{geo_score})
- Access model: {access_reason} (+{access_score})

⚖️ Interpretation:
{score_reason}

🧠 Decision Summary:
{synthesis}
"""

    return explanation.strip()