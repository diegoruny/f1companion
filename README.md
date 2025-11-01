# F1 Race Companion

F1 Race Companion is a Python desktop application that provides real-time Formula 1 racing information including driver standings, constructor standings, and upcoming race details. The application features a modern GUI built with Tkinter and integrates with the Ergast F1 API to fetch live racing data.

## Features

- **Driver Standings**: View current season driver championship standings with positions, points, nationality, and teams
- **Constructor Standings**: Track constructor championship standings with wins and points
- **Next Race Information**: See details about the upcoming F1 race including circuit, location, date, and time
- **Last Race Results**: View podium finishers and details from the most recent race
- **Data Caching**: Intelligent caching system reduces API calls and improves performance
- **Real-time Updates**: Fetches live data from the Ergast F1 API

## Technology Stack

- **Python**: 3.7+
- **GUI Framework**: 
  - Tkinter (built-in Python GUI library)
  - ttkbootstrap (modern styling for Tkinter widgets)
  - sv-ttk (Silicon Valley theme)
- **Data Processing**: pandas
- **API Integration**: requests
- **Optional**: pygame (for race simulation features - experimental)

## Installation

1. Ensure you have Python 3.7 or higher installed on your system.

2. Clone this repository:
   ```bash
   git clone https://github.com/diegoruny/f1companion.git
   cd f1companion
   ```

3. (Recommended) Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the F1 Race Companion, execute the following command in the project root directory:

```bash
python main.py
```

The application will launch with a window displaying:
- Top bar with last race and next race information
- Tabbed interface with Driver Standings and Constructor Standings

## Project Structure

```
├── main.py                    # Application entry point
├── api/
│   ├── api_handler.py        # Ergast F1 API wrapper
│   └── localData/            # Local CSV race data files
├── ui/
│   ├── dashboard.py          # Main dashboard container
│   ├── list_builder.py       # Driver standings widget
│   ├── constructors_standings.py  # Constructor standings widget
│   ├── next_race.py          # Next/last race cards
│   └── top_Bar.py            # Top navigation bar
└── utils/
    ├── last_race_sim_data.py  # Race simulation (experimental)
    └── sprites/               # Car images for simulation
```

## Requirements

- Python 3.7 or higher
- Internet connection for API calls (data is cached locally)
- All dependencies listed in `requirements.txt`

## Known Limitations

- Race simulation features are experimental and not fully integrated into the main UI
- Application requires internet connection to fetch initial data (subsequent requests use cached data)
- Some features may not work during F1 off-season when no races are scheduled

## Contributing

This is a personal portfolio project. If you find any issues or have suggestions, feel free to open an issue or submit a pull request.

## License

This project is open source and available for personal and educational use.

