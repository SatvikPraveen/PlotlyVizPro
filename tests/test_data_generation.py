"""
Tests for generate_datasets.py

Validates that dataset generation works correctly.
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDatasetGeneration:
    """Test dataset generation functions"""
    
    def test_datasets_directory_exists(self):
        """Test that datasets directory exists"""
        datasets_dir = Path(__file__).parent.parent / 'datasets'
        assert datasets_dir.exists()
        assert datasets_dir.is_dir()
    
    def test_required_datasets_exist(self):
        """Test that all required datasets exist"""
        datasets_dir = Path(__file__).parent.parent / 'datasets'
        required_files = [
            'superstore.csv',
            'covid_data.csv',
            'stock_data.csv',
            'customer_segments.csv',
            'world_population.csv',
            'map_data.csv',
            'animated_sales.csv',
            'product_launch.csv'
        ]
        
        for filename in required_files:
            file_path = datasets_dir / filename
            assert file_path.exists(), f"Missing dataset: {filename}"
    
    def test_superstore_dataset_structure(self):
        """Test superstore dataset has correct structure"""
        datasets_dir = Path(__file__).parent.parent / 'datasets'
        df = pd.read_csv(datasets_dir / 'superstore.csv')
        
        # Check required columns exist
        required_columns = ['OrderID', 'OrderDate', 'Category', 'SubCategory', 'Region', 'Sales', 'Profit']
        for col in required_columns:
            assert col in df.columns, f"Missing column: {col}"
        
        # Check data types
        assert df['Sales'].dtype in [float, int]
        assert df['Profit'].dtype in [float, int]
        assert len(df) > 0
    
    def test_covid_dataset_structure(self):
        """Test COVID dataset has correct structure"""
        datasets_dir = Path(__file__).parent.parent / 'datasets'
        df = pd.read_csv(datasets_dir / 'covid_data.csv')
        
        # Check it has data
        assert len(df) > 0
        
        # Check for common columns (exact names may vary)
        assert any(col.lower() in ['date', 'country', 'cases', 'deaths'] for col in df.columns)


class TestDatasetQuality:
    """Test quality of generated datasets"""
    
    def test_no_empty_datasets(self):
        """Ensure no dataset is empty"""
        datasets_dir = Path(__file__).parent.parent / 'datasets'
        
        for csv_file in datasets_dir.glob('*.csv'):
            df = pd.read_csv(csv_file)
            assert len(df) > 0, f"Empty dataset: {csv_file.name}"
    
    def test_datasets_have_headers(self):
        """Ensure all datasets have proper headers"""
        datasets_dir = Path(__file__).parent.parent / 'datasets'
        
        for csv_file in datasets_dir.glob('*.csv'):
            df = pd.read_csv(csv_file)
            assert len(df.columns) > 0, f"No columns in: {csv_file.name}"
            assert not df.columns[0].startswith('Unnamed'), f"Missing headers: {csv_file.name}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
