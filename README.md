# 🌿 GreenTrace AI

**GreenTrace AI** is an AI-powered environmental monitoring web application that leverages satellite data and advanced language models to track and analyze the greenery (NDVI) of any geographic area. 

Through this platform, users can visualize a **Past vs. Present** historical comparison to accurately understand how much green cover has been lost or gained over the years in their selected location.

---

## 🚀 Key Features

- **Satellite-Driven NDVI Analysis:** Utilizes Google Earth Engine (GEE) and Landsat 8 satellite imagery to calculate exact greenery percentages (NDVI).
- **Dynamic Year Selection:** Users can select any historical year (e.g., 2000, 2016) from the frontend and compare it with the current year.
- **Sarvam AI Insights:** Integrates Sarvam AI to translate complex satellite metrics into easy-to-understand, actionable climate insights.
- **Graph Database Storage:** Uses a Neo4j Graph Database to efficiently map, store, and query environmental trends across different areas.
- **Interactive Map UI:** Features a Leaflet Map integration, allowing users to seamlessly select and visualize their region of interest.

---

## 🛠️ Tech Stack

- **Frontend:** React.js, Vite, Tailwind CSS, Leaflet Map
- **Backend:** FastAPI (Python), Uvicorn
- **Satellite Engine:** Google Earth Engine (GEE) Python API
- **AI Model:** Sarvam AI API
- **Database:** Neo4j (Graph Database)

---

## 📁 Project Structure

```text
hackhazard-project/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI core endpoints
│   │   ├── sat_engine.py           # GEE Integration & NDVI Logic
│   │   ├── ai_logic.py             # Sarvam AI Prompting
│   │   └── db_helper.py            # Neo4j Database handler
│   └── requirements.txt            # Backend Python dependencies
└── frontend/
    ├── src/
    │   ├── components/             # Map & UI Layouts
    │   ├── App.jsx                 # Frontend State & API Calls
    │   ├── main.jsx                # App Entry point
    │   └── index.css               # Tailwind styling
    └── package.json                # Frontend dependencies
```
## Live link- https://hackhazard-project.vercel.app/
