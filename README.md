# ⚾ Playball — Your Ultimate Game-Day Companion!

Playball is a Python-based dashboard designed for **Major League Baseball (MLB)** fans to simplify game-day planning.  
It aggregates key information such as **game schedules**, **weather forecasts**, and **nearby local restaurants** into one intuitive interface — helping users save time and enhance their game-day experience.

---

## 🎯 Vision

**Your Ultimate Game-Day Companion!**  
Playball aims to eliminate the hassle of juggling multiple tabs and sources when planning to attend a baseball game.
<img width="513" height="334" alt="Screenshot 2025-10-28 at 17 34 13" src="https://github.com/user-attachments/assets/21021c8a-983a-4978-b9bd-5acb1fd56ee6" />


---

## 🧩 Problem & Solution

| Problem | Solution |
|----------|-----------|
| Time-consuming and inefficient to find all game-day info across different websites. | One unified dashboard displaying schedules, weather, and nearby food options. |
| Current approach: manually searching through multiple websites. | Centralized data view saves time and enhances user experience. |

---

## 🖥️ Features

✅ **Game Schedule Integration**  
Pulls MLB matchups, team names, venues, and game dates.

☀️ **Weather Forecasting**  
Displays up-to-date temperature, humidity, and precipitation for each stadium city.

🍔 **Nearby Restaurants**  
Shows local dining options near the stadium (address, phone, and ratings).

📊 **Dashboard Interface**  
A clean, tabular view displaying all information side-by-side.

---

## ⚙️ How It Works

### 1. Data Collection
Each module fetches specific data:
- **`data_mlb.py`** → MLB game schedule (teams, venues, times)  
- **`data_weather.py`** → WeatherAPI forecast by city  
- **`data_places.py`** → Nearby restaurants from Google Places  
- **`data_stadium.py`** → Stadium metadata (location, capacity)

### 2. Data Integration
`main.py` merges all sources into a unified Pandas DataFrame, then displays the dashboard combining:
- Match info  
- Real-time weather  
- Recommended nearby restaurants  

### 3. Output Example

| Date | City | Stadium | Weather | Avg Temp (°F) | Top Restaurants |
|------|------|----------|----------|----------------|-----------------|
| Oct 8, 2024 | Pittsburgh | PNC Park | Clear | 53.1 | Tooty’s Hamburgers, Lafayette Coney Island |

---

## 🧰 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Playball.git
   cd Playball
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Set up environment variables**
   ```bash
   WEATHER_API_KEY=your_weatherapi_key
   GOOGLE_PLACES_API_KEY=your_google_places_key
4. **Run the app**
   ```bash
   python scripts/main.py

---
## 📸 Dashboard Preview

<img width="1013" height="561" alt="Screenshot 2025-10-28 at 17 34 44" src="https://github.com/user-attachments/assets/d3f72de9-9891-48cc-bb73-1b7372bc924f" />
