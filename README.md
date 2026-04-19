# 🌍 COMS AI - Community Opportunity Mapping System

## 📌 Live App
👉 https://coms-ai-fadil-ade.streamlit.app/

---

## 📸 App Preview

![COMS Screenshot](screenshot.jpeg)

---

## 🧠 About the Project

**COMS AI (Community Opportunity Mapping System)** is an AI-powered platform that helps users discover, analyze, and evaluate opportunities based on their:

- Field of interest (Tech, Business, Social, Policy)
- Skill level (Beginner → Advanced)
- Location (Local, Africa, Global, Remote)

It uses an intelligent scoring system to rank opportunities and generate personalized recommendations.

---

## 🚀 Key Features

### 🧠 AI Opportunity Matching
Automatically matches users with relevant opportunities.

### 🏆 Smart Ranking System
Scores each opportunity using:
- Skill alignment
- Accessibility
- Geographic relevance
- Progression potential

### 📊 Committee-Level Evaluation
Simulates real selection logic like scholarship committees.

### 📍 Local & Global Mapping
Visualizes opportunities across different regions.

### 📄 AI Impact Report Generator
Generates downloadable PDF reports using ReportLab.

### 🏆 Leadership Narrative Generator
Creates a personalized summary for users.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- ReportLab
- Folium (map visualization)
- Streamlit PDF Viewer

---

## 📂 Project Structure

app.py
modules/
-├── data_loader.py
-├── matcher.py
-├── map_view.py
-├── analyzer.py
-├── explainer.py
-├── report.py
-├── scorer.py

---

## 📄 Installation (Local Setup)

```bash
git clone https://github.com/your-username/coms-ai.git
cd coms-ai

pip install -r requirements.txt

streamlit run app.py
```

---

## 📦 Requirements

streamlit
pandas
reportlab
streamlit-pdf-viewer
folium
streamlit-folium

---

## 🎯 Purpose of the Project

This project was built to simulate:

- Scholarship selection systems
- Opportunity evaluation frameworks
- AI-based decision-making tools

It demonstrates skills in:

- Data processing
- AI logic design
- UI/UX design with Streamlit
- PDF report generation
- Geospatial visualization

---

## 👤 Author

Fadil Owolara ADELABOU
AI & Software Development Enthusiast

---

## ⭐ Future Improvements

- Add machine learning-based scoring model
- Improve recommendation engine
- Add user authentication
- Deploy scalable backend API

---

# 🚀 🧠 DEPLOYMENT CHECKLIST (STREAMLIT CLOUD)

Your app is already deployed here:
👉 https://coms-ai-fadil-ade.streamlit.app/

Now just ensure:

---

## ✅ 1. GitHub repo is updated

```bash
git add .
git commit -m "Final deployment version"
git push
```

## ✅ 2. Requirements file is correct
✔ Must include:
streamlit
pandas
reportlab
streamlit-pdf-viewer
folium
streamlit-folium

## 3. No venv pushed (IMPORTANT)
✔ .gitignore contains
venv/
__pycache__/
