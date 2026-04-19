from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_report(user_field, user_level, user_location, insights):

    buffer = BytesIO()  # 📦 memory file instead of disk
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    content = []

    # 🏆 TITLE
    title = Paragraph("Community Opportunity Impact Report", styles["Title"])
    content.append(title)
    content.append(Spacer(1, 0.2 * inch))

    # 📌 PROFILE
    profile = Paragraph(
        f"<b>User Profile</b><br/>"
        f"Field: {user_field}<br/>"
        f"Level: {user_level}<br/>"
        f"Location: {user_location}",
        styles["Normal"]
    )
    content.append(profile)
    content.append(Spacer(1, 0.3 * inch))

    # 📊 SUMMARY
    summary_text = f"""
    This report analyzes opportunities for {user_field} at {user_level} level in {user_location}.
    """

    content.append(Paragraph("<b>Executive Summary</b><br/>" + summary_text, styles["Normal"]))
    content.append(Spacer(1, 0.3 * inch))

    # 🧠 INSIGHTS
    insights_text = "<br/>".join(insights)
    content.append(Paragraph("<b>Key Insights</b><br/>" + insights_text, styles["Normal"]))
    content.append(Spacer(1, 0.3 * inch))

    # 🚀 RECOMMENDATIONS
    recommendations = """
    - Apply to global opportunities<br/>
    - Improve skills for higher-level access<br/>
    - Focus on remote programs
    """

    content.append(Paragraph("<b>Recommendations</b><br/>" + recommendations, styles["Normal"]))

    # 📄 BUILD PDF
    doc.build(content)

    buffer.seek(0)
    return buffer