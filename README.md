# F1 Race Companion

A Python desktop application for viewing Formula 1 racing information including driver standings, constructor standings, and race details. Features a modern GUI built with Tkinter.

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## ✨ Features

- **Driver Standings**: View current season driver championship standings with positions, points, nationality, and teams
- **Constructor Standings**: Track constructor championship standings with wins and points
- **Next Race Information**: See details about upcoming F1 races
- **Last Race Results**: View podium finishers and details from the most recent race
- **Offline Mode**: Works without internet using bundled 2024 season data
- **Modern UI**: Clean interface with ttkbootstrap theming

## 🖥️ Screenshots

*Coming soon*

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.7+ |
| **GUI** | Tkinter, ttkbootstrap, sv-ttk |
| **Data** | pandas |
| **API** | requests (optional, for live data) |

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/diegoruny/f1companion.git
   cd f1companion
   ```

2. **Create virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

```bash
python main.py
```

The application launches with:
- Top bar showing last race and next race information
- Tabbed interface with Driver Standings and Constructor Standings

## 📁 Project Structure

```
f1companion/
├── main.py                     # Application entry point
├── api/
│   ├── csv_handler.py          # Offline data handler (CSV/JSON)
│   ├── api_handler.py          # Online API handler (deprecated)
│   ├── cache_manager.py        # Cache management
│   └── config.py               # API configuration
├── ui/
│   ├── dashboard.py            # Main dashboard container
│   ├── list_builder.py         # Driver standings widget
│   ├── constructors_standings.py  # Constructor standings widget
│   ├── next_race.py            # Next/last race cards
│   └── top_Bar.py              # Top navigation bar
├── utils/
│   └── sprites/                # Car images
├── final_race_data.csv         # Race results data
├── current_drivers_standings.json  # Standings data
└── requirements.txt
```

## 🔄 Data Modes

### Offline Mode (Default)
The app now runs in **offline mode** by default, using bundled 2024 season data:
- `final_race_data.csv` - Race results and lap data
- `current_drivers_standings.json` - Driver/constructor standings

No internet connection required!

### Online Mode (Deprecated)
The original Ergast F1 API is no longer available. The `api_handler.py` is kept for reference but the app now uses `csv_handler.py` for all data.

## 📋 Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`:
  - pandas >= 2.0.0
  - requests >= 2.31.0
  - ttkbootstrap >= 1.10.0
  - sv-ttk >= 2.0.0

## 🐛 Known Limitations

- Race simulation features are experimental
- Data is from 2024 season (static, not live)
- Some date/time fields show placeholder values in offline mode

## 🤝 Contributing

This is a personal portfolio project. Issues and pull requests are welcome!

## 📄 License

This project is open source and available for personal and educational use.

---

*Built with ❤️ by [Diego Delgado Torres](https://github.com/diegoruny)*
