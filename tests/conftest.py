"""Pytest configuration and shared fixtures."""

import json
import os
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory with test CSV/JSON files."""
    # Create test race data CSV
    race_data = pd.DataFrame({
        'raceId': [1, 2],
        'grandPrix': ['Bahrain Grand Prix', 'Saudi Arabian Grand Prix'],
        'officialEventName': ['FORMULA 1 GULF AIR BAHRAIN GRAND PRIX 2024',
                              'FORMULA 1 STC SAUDI ARABIAN GRAND PRIX 2024'],
        'country': ['Bahrain', 'Saudi Arabia'],
        'location': ['Sakhir', 'Jeddah'],
        'circuit': ['Bahrain International Circuit',
                    'Jeddah Corniche Circuit'],
        'winner': ['Max Verstappen', 'Max Verstappen'],
        'team': ['Red Bull Racing', 'Red Bull Racing'],
        'laps': [57, 50],
        'time': ['1:31:44.742', '1:20:43.273']
    })
    race_csv_path = tmp_path / 'final_race_data.csv'
    race_data.to_csv(race_csv_path, index=False)

    # Create test standings JSON
    standings_data = {
        'season': '2024',
        'round': '2',
        'DriverStandings': [
            {
                'position': '1',
                'points': '51',
                'wins': '2',
                'Driver': {
                    'driverId': 'max_verstappen',
                    'givenName': 'Max',
                    'familyName': 'Verstappen',
                    'permanentNumber': '1'
                },
                'Constructors': [{'name': 'Red Bull'}]
            },
            {
                'position': '2',
                'points': '28',
                'wins': '0',
                'Driver': {
                    'driverId': 'perez',
                    'givenName': 'Sergio',
                    'familyName': 'Pérez',
                    'permanentNumber': '11'
                },
                'Constructors': [{'name': 'Red Bull'}]
            }
        ]
    }
    standings_json_path = tmp_path / 'current_drivers_standings.json'
    with open(standings_json_path, 'w', encoding='utf-8') as f:
        json.dump(standings_data, f)

    return tmp_path


@pytest.fixture
def csv_handler(test_data_dir):
    """Create a CSVDataHandler instance with test data."""
    from api.csv_handler import CSVDataHandler
    return CSVDataHandler(data_dir=str(test_data_dir))
