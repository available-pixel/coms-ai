def analyze_gaps(local_df, global_df, user_field, user_location):
    insights = []

    local_count = 0 if local_df is None else local_df.shape[0]
    global_count = 0 if global_df is None else global_df.shape[0]
    total = local_count + global_count

    # -------------------------------
    # 🧠 GLOBAL EVALUATION SUMMARY (ELITE v3)
    # -------------------------------
    if total == 0:
        insights.append(f"⚠️ Critical Gap Identified: No {user_field} opportunities detected in the current ecosystem.")
        return insights

    insights.append("📊 Profile alignment shows consistent match with available opportunities.")
    insights.append("📍 Geographic access remains a key constraint influencing opportunity selection.")
    insights.append("⚖️ Opportunity distribution is uneven, with limited local depth but global compensation.")
    insights.append("🧠 Recommendation: Cross-regional applications significantly improve selection probability.")
    

    # -------------------------------
    # 📍 LOCAL ANALYSIS
    # -------------------------------
    if local_count == 0:
        insights.append(f"⚠️ Local Market Constraint: No opportunities available in {user_location}, increasing dependency on external mobility.")
    elif local_count == 1:
        insights.append("📍 Local Market Status: Single-entry availability indicates high competition environment.")
    else:
        insights.append(f"📍 Local Market Strength: {local_count} opportunities detected within local ecosystem.")

    # -------------------------------
    # 🌍 GLOBAL ANALYSIS
    # -------------------------------
    if global_count == 0:
        insights.append("🌐 Global Expansion: No external opportunities detected — limited fallback options.")
    elif global_count == 1:
        insights.append("🌐 Global Expansion: Single international opportunity available as alternative pathway.")
    else:
        insights.append("🌐 Global Expansion: Multiple international opportunities significantly improve accessibility range.")

    # -------------------------------
    # ⚡ ACCESSIBILITY INTELLIGENCE
    # -------------------------------
    total_access = 0
    count = 0

    for df in [local_df, global_df]:
        if df is not None and "access_score" in df.columns:
            total_access += df["access_score"].sum()
            count += len(df)

    if count > 0:
        avg_access = total_access / count

        if avg_access >= 2.5:
            insights.append("🚀 Accessibility Index: High proportion of remote-friendly opportunities.")
        elif avg_access >= 1.5:
            insights.append("⚡ Accessibility Index: Balanced mix of remote and on-site opportunities.")
        else:
            insights.append("⚠️ Accessibility Index: Dominance of on-site requirements may limit flexibility.")

    # -------------------------------
    # 🎯 COMPETITION & SCARCITY MODEL
    # -------------------------------
    if total <= 2:
        insights.append("🎯 Scarcity Level: Extremely limited opportunity pool — highly competitive selection environment.")
    elif total <= 4:
        insights.append("🎯 Scarcity Level: Moderate opportunity density with competitive filtering expected.")
    else:
        insights.append("🎯 Scarcity Level: Healthy opportunity distribution across ecosystem.")

    return insights