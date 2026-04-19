import folium
from streamlit_folium import st_folium

# 🌍 Realistic coordinates
LOCATION_COORDS = {
    "Benin": [6.3703, 2.3912],
    "Ethiopia": [9.1450, 40.4897],
    "USA": [37.0902, -95.7129],
    "Multiple": [10, 20],
    "Remote": [20, 0],
    "Global": [20, 0]
}

# 🎨 Color by geo level
GEO_COLORS = {
    "Local": "green",
    "Regional": "blue",
    "Global": "red"
}


def get_coordinates(row):
    # Priority: country → location fallback
    country = row.get("country", "Global")
    return LOCATION_COORDS.get(country, LOCATION_COORDS.get(row["location"], [20, 0]))


def render_map(opportunities, location="Global"):
    # 🌍 Center map based on user location
    center_coords = LOCATION_COORDS.get(location, [20, 0])

    m = folium.Map(location=center_coords, zoom_start=3)

    # 🧠 Add markers with intelligence
    for _, row in opportunities.iterrows():
        coords = get_coordinates(row)

        color = GEO_COLORS.get(row.get("geo_level", "Global"), "gray")
        score = row.get("match_score", 0)

        popup_text = f"""
        <b>{row['title']}</b><br>
        Provider: {row['provider']}<br>
        Type: {row['type']}<br>
        Field: {row['field']}<br>
        Score: {score}/100<br>
        Mode: {row['mode']}<br>
        """

        folium.CircleMarker(
            location=coords,
            radius=6 + (score / 20),  # size based on score
            popup=popup_text,
            tooltip=row["title"],
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    return st_folium(m, width=750, height=500)