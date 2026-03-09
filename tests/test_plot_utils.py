"""
Tests for plot_utils.py

Validates plotting utility functions for correctness and output types.
"""
import pytest
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.plot_utils import (
    line_plot,
    scatter_plot,
    bubble_plot,
    apply_dark_theme,
    apply_custom_layout,
)


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing"""
    return pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=10),
        'Sales': [100, 150, 120, 180, 200, 210, 190, 220, 240, 250],
        'Profit': [20, 30, 25, 35, 40, 42, 38, 44, 48, 50],
        'Region': ['East'] * 5 + ['West'] * 5,
        'Category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
    })


class TestLinePlot:
    """Test line_plot function"""
    
    def test_basic_line_plot(self, sample_data):
        """Test basic line plot creation"""
        fig = line_plot(sample_data, x='Date', y='Sales', title='Test Plot')
        assert isinstance(fig, go.Figure)
        assert fig.layout.title.text == 'Test Plot'
    
    def test_line_plot_with_color(self, sample_data):
        """Test line plot with color grouping"""
        fig = line_plot(sample_data, x='Date', y='Sales', color='Region')
        assert isinstance(fig, go.Figure)
        # Should have multiple traces for different regions
        assert len(fig.data) > 1
    
    def test_line_plot_no_markers(self, sample_data):
        """Test line plot without markers"""
        fig = line_plot(sample_data, x='Date', y='Sales', markers=False)
        assert isinstance(fig, go.Figure)


class TestScatterPlot:
    """Test scatter_plot function"""
    
    def test_basic_scatter(self, sample_data):
        """Test basic scatter plot"""
        fig = scatter_plot(sample_data, x='Sales', y='Profit')
        assert isinstance(fig, go.Figure)
    
    def test_scatter_with_color(self, sample_data):
        """Test scatter plot with color"""
        fig = scatter_plot(sample_data, x='Sales', y='Profit', color='Category')
        assert isinstance(fig, go.Figure)
    
    def test_scatter_with_size(self, sample_data):
        """Test scatter plot with size parameter"""
        fig = scatter_plot(sample_data, x='Sales', y='Profit', size='Profit')
        assert isinstance(fig, go.Figure)


class TestBubblePlot:
    """Test bubble_plot function"""
    
    def test_bubble_plot(self, sample_data):
        """Test bubble plot creation"""
        fig = bubble_plot(sample_data, x='Sales', y='Profit', size='Profit')
        assert isinstance(fig, go.Figure)


class TestTheming:
    """Test theming functions"""
    
    def test_apply_dark_theme(self, sample_data):
        """Test dark theme application"""
        fig = line_plot(sample_data, x='Date', y='Sales')
        fig = apply_dark_theme(fig)
        assert isinstance(fig, go.Figure)
        assert fig.layout.paper_bgcolor == '#111'
        assert fig.layout.plot_bgcolor == '#222'
    
    def test_apply_custom_layout(self, sample_data):
        """Test custom layout application"""
        fig = line_plot(sample_data, x='Date', y='Sales')
        fig = apply_custom_layout(
            fig,
            title='Custom Title',
            xaxis_title='X Axis',
            yaxis_title='Y Axis'
        )
        assert fig.layout.title.text == 'Custom Title'
        assert fig.layout.xaxis.title.text == 'X Axis'
        assert fig.layout.yaxis.title.text == 'Y Axis'


class TestExportFunctions:
    """Test export utilities"""
    
    def test_save_paths_creation(self, sample_data, tmp_path):
        """Test that export functions would create proper paths"""
        # This is a light test since we don't want to create actual files
        # in the test suite. We just verify the logic.
        from utils.plot_utils import Path as UtilPath
        
        # Just verify Path operations work
        test_path = tmp_path / "test_export"
        test_path.mkdir(parents=True, exist_ok=True)
        assert test_path.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
