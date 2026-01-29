"""Unit tests for CSVDataHandler - Basic functionality only."""

import pytest


@pytest.mark.unit
class TestCSVDataHandler:
    """Test suite for CSVDataHandler class - basic unit tests."""

    def test_initialization(self, csv_handler, test_data_dir):
        """Test handler initializes with correct paths."""
        assert csv_handler.data_dir == str(test_data_dir)
        assert csv_handler.race_data_path.endswith('final_race_data.csv')
        assert csv_handler.standings_path.endswith('current_drivers_standings.json')

    def test_load_race_data(self, csv_handler):
        """Test loading race data from CSV."""
        df = csv_handler._load_race_data()
        
        assert len(df) == 2
        assert 'grandPrix' in df.columns
        assert 'winner' in df.columns
        # Check we have at least raceId column
        assert 'raceId' in df.columns

    def test_race_data_caching(self, csv_handler):
        """Test that race data is cached after first load."""
        df1 = csv_handler._load_race_data()
        df2 = csv_handler._load_race_data()
        
        # Should return the same cached object
        assert df1 is df2

    def test_load_standings_data(self, csv_handler):
        """Test loading standings data from JSON."""
        data = csv_handler._load_standings_data()
        
        assert 'season' in data
        assert data['season'] == '2024'
        assert 'DriverStandings' in data
        assert len(data['DriverStandings']) == 2

    def test_standings_data_caching(self, csv_handler):
        """Test that standings data is cached after first load."""
        data1 = csv_handler._load_standings_data()
        data2 = csv_handler._load_standings_data()
        
        # Should return the same cached object
        assert data1 is data2

    def test_missing_race_data_file(self, tmp_path):
        """Test handling of missing race data file."""
        from api.csv_handler import CSVDataHandler
        
        handler = CSVDataHandler(data_dir=str(tmp_path))
        
        with pytest.raises(FileNotFoundError):
            handler._load_race_data()

    def test_missing_standings_file(self, tmp_path):
        """Test handling of missing standings file."""
        from api.csv_handler import CSVDataHandler
        
        # Create only race data, not standings
        import pandas as pd
        race_data = pd.DataFrame({'grandPrix': ['Test GP'], 'raceId': [1]})
        race_csv_path = tmp_path / 'final_race_data.csv'
        race_data.to_csv(race_csv_path, index=False)
        
        handler = CSVDataHandler(data_dir=str(tmp_path))
        
        with pytest.raises(FileNotFoundError):
            handler._load_standings_data()

