import pandas as pd
import os

REQUIRED_COLUMNS = [
    "id", "title", "provider", "type", "field", "level",
    "location", "country", "mode", "deadline",
    "eligibility", "description", "link"
]


def load_data():
    # 📁 Build path safely
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data", "opportunities.csv")

    # 📊 Load CSV
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise Exception("❌ opportunities.csv file not found")

    # 🧠 Validate structure
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise Exception(f"❌ Missing required columns: {missing_cols}")

    # 🧹 Clean data
    df = clean_data(df)

    # 🧠 Enrich data (important for later modules)
    df = enrich_data(df)

    return df


# -------------------------------
# 🧹 CLEANING FUNCTION
# -------------------------------
def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates(subset=["id"])

    # Strip whitespace
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()

    # Normalize casing
    df["field"] = df["field"].str.title()
    df["level"] = df["level"].str.title()
    df["type"] = df["type"].str.title()
    df["location"] = df["location"].str.title()
    df["mode"] = df["mode"].str.title()

    # Fill missing values
    df["country"] = df["country"].fillna("Unknown")
    df["deadline"] = df["deadline"].fillna("Unknown")
    df["eligibility"] = df["eligibility"].fillna("Not specified")
    df["description"] = df["description"].fillna("No description available")

    return df


# -------------------------------
# 🧠 ENRICHMENT FUNCTION
# -------------------------------
def enrich_data(df):
    # 🌍 Geographic level classification
    def classify_geo(loc):
        if loc == "Benin":
            return "Local"
        elif loc == "Africa":
            return "Regional"
        elif loc in ["Global", "Remote"]:
            return "Global"
        else:
            return "Other"

    df["geo_level"] = df["location"].apply(classify_geo)

    # 🌐 Accessibility score (basic logic)
    def accessibility(mode):
        if mode == "Remote":
            return 3
        elif mode == "Hybrid":
            return 2
        else:
            return 1

    df["access_score"] = df["mode"].apply(accessibility)

    return df