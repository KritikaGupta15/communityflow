# 🏙️ CommunityFlow Chicago

> An AI-integrated geospatial intelligence dashboard designed for yoga instructors and community wellness leaders to analyze neighborhood viability, explore civic metrics, and query intelligent advisors across Chicago.

---

## ✨ Key Features

- **Interactive Geospatial Mapping**: Dynamic Leaflet.js mapping with custom neighborhood markers, live zoom controls, and instant visual feedback.
- **Advanced Neighborhood Filtering**: Filter Chicago neighborhoods dynamically by minimum transit scores, park counts, and library availability.
- **Conversational AI Assistant**: Ask natural language questions (e.g., *"Where should I teach yoga?"*) to receive tailored recommendations.
- **AI-Driven Neighborhood Reports**: Instant generative AI summaries analyzing population density, wellness scores, and community infrastructure for any selected neighborhood.
- **Free Tier API Resilience & Caching**: Engineered with intelligent front-end memory caching and backend rate-limit fallbacks (smart database-driven defaults) to ensure uninterrupted uptime under strict Google Gemini Free Tier quotas.
- **Data Export**: Built-in CSV export to download filtered neighborhood datasets instantly.

---

## 🏗️ Architecture & System Design

CommunityFlow Chicago is structured as a decoupled full-stack application optimized for low-latency spatial data retrieval and resilient AI generation.

```text
 ┌──────────────────────┐         HTTP / REST         ┌────────────────────────┐
 │                      │ ──────────────────────────> │                        │
 │    React + Vite      │                             │     FastAPI Backend    │
 │   Frontend (UI/Map)  │ <────────────────────────── │  (Endpoints & Routers) │
 │                      │         JSON Data           │                        │
 └──────────────────────┘                             └───────────┬────────────┘
            │                                                     │
            │ (Client Caching)                                    │ (SQLAlchemy ORM)
            ▼                                                     ▼
   [summaryCache / chatCache]                             ┌────────────────────────┐
                                                          │   PostgreSQL Database  │
                                                          │  (Spatial & Civic Data)│
                                                          └────────────────────────>
                                                                  │
                                                                  │ (LLM Fallbacks)
                                                                  ▼
                                                          ┌────────────────────────┐
                                                          │   Google Gemini API    │
                                                          │  (gemini-3.8-flash)    │
                                                          └────────────────────────┘

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python, SQLAlchemy, PostgreSQL (Spatial Data)
- **Frontend**: React, Vite, Leaflet.js / React-Leaflet, Axios
- **AI & LLM**: Google Gemini API (`gemini-3.8-flash`) with custom caching and rate-limit recovery
- **Styling**: Modern CSS, Flexbox, Responsive UI

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.10+
- Node.js & npm
- PostgreSQL installed and running locally

### 1. Clone the Repository
```bash
git clone [https://github.com/KritikaGupta15/communityflow.git](https://github.com/KritikaGupta15/communityflow.git)
cd communityflow
