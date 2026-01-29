"""Integration tests for CSVDataHandler using real project data."""

import os
import pytest


@pytest.fixture
def project_root():
    """Get the project root directory."""
    # tests/ is one level down from root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def real_csv_handler(project_root):
    """Create CSVDataHandler with real project data."""
    from api.csv_handler import CSVDataHandler
    
    # Skip test if real data files don't exist
    race_data_path = os.path.join(project_root, 'final_race_data.csv')
    standings_path = os.path.join(project_root, 'current_drivers_standings.json')
    
    if not os.path.exists(race_data_path) or not os.path.exists(standings_path):
        pytest.skip("Real data files not found - skipping integration tests")
    
    return CSVDataHandler(data_dir=project_root)


@pytest.mark.integration
class TestCSVDataHandlerIntegration:
    """Integration tests with real data files."""

    def test_load_real_race_data(self, real_csv_handler):
        """Test loading actual race data CSV."""
        df = real_csv_handler._load_race_data()
        
        assert len(df) > 0, "Race data should not be empty"
        
        # Check expected columns exist
        required_cols = ['raceId', 'driverId', 'circuitRef', 'country']
        for col in required_cols:
            assert col in df.columns, f"Missing required column: {col}"

    def test_get_real_driver_standings(self, real_csv_handler):
        """Test getting actual driver standings."""
        standings = real_csv_handler.get_driver_standings()
        
        assert isinstance(standings, list), "Should return a list"
        
        if len(standings) > 0:
            first = standings[0]
            # Check actual keys returned by CSVDataHandler
            assert 'NAME' in first or 'Driver' in first
            assert 'NUMBER' in first or 'permanentNumber' in first

    def test_get_real_constructor_standings(self, real_csv_handler):
        """Test getting actual constructor standings."""
        standings = real_csv_handler.get_constructor_standings()
        
        assert standings is not None
        assert len(standings) > 0, "Should have constructor standings"

    def test_get_real_race_results(self, real_csv_handler):
        """Test getting actual race results."""
        # Get all results first
        all_results = real_csv_handler.get_race_results()
        assert isinstance(all_results, list)
        
        if len(all_results) > 0:
            # Get results for first race
            first_race_id = all_results[0].get('raceId')
            if first_race_id:
                race_results = real_csv_handler.get_race_results(race_id=first_race_id)
                assert len(race_results) > 0

    def test_get_real_next_race(self, real_csv_handler):
        """Test getting next race from actual data."""
        next_race = real_csv_handler.get_next_race()
        
        # May be None if season is over
        if next_race is not None:
            assert 'circuit' in next_race
            assert 'location' in next_race or 'country' in next_race

    def test_get_real_circuits(self, real_csv_handler):
        """Test getting circuits from actual data."""
        circuits = real_csv_handler.get_circuits()
        
        assert isinstance(circuits, list)
        assert len(circuits) > 0, "Should have at least one circuit"
        
        first = circuits[0]
        assert 'circuit_id' in first or 'circuitId' in first
        # Circuit name might not be in the dict - it's derived from other data
        assert 'country' in first

    def test_get_real_season_info(self, real_csv_handler):
        """Test getting season information."""
        info = real_csv_handler.get_season_info()
        
        assert 'season' in info
        assert 'data_source' in info

    def test_get_real_last_race(self, real_csv_handler):
        """Test getting last race information."""
        race_info, results = real_csv_handler.get_last_race()
        
        # May be None if no completed races
        if race_info is not None:
            assert 'circuit' in race_info or 'circuitName' in race_info
            assert 'location' in race_info or 'country' in race_info
        
        if results is not None:
            assert isinstance(results, list)
