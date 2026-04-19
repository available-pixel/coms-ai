def match_opportunities(df, user_field, user_level, user_location):

    user_field = user_field.title()
    user_level = user_level.title()
    user_location = user_location.title()

    # 🧠 STEP 1: SCORE ALL DATA FIRST
    def compute_match_score(row):
        score = 0

        # Field
        if row["field"] == user_field:
            score += 40
        else:
            score += 10

        # Level
        if row["level"] == user_level:
            score += 30
        else:
            score += 15

        # Geo
        if user_location == "Benin":
            if row["location"] == "Benin":
                score += 25
            elif row["location"] == "Africa":
                score += 20
            else:
                score += 10

        elif user_location == "Africa":
            if row["location"] == "Africa":
                score += 25
            else:
                score += 15
        else:
            score += 15

        score += row.get("access_score", 0) * 5

        return min(score, 100)

    df = df.copy()
    df["match_score"] = df.apply(compute_match_score, axis=1)

    # 🏆 STEP 2: FILTER AFTER SCORING (IMPORTANT CHANGE)
    df = df[df["match_score"] > 30]

    # 🧠 STEP 3: SPLIT
    local_matches = df[df["location"].isin(["Benin", "Africa"])].sort_values("match_score", ascending=False)
    global_matches = df[df["location"] == "Global"].sort_values("match_score", ascending=False)

    return local_matches, global_matches