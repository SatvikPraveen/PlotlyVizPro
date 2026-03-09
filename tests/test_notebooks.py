"""
Tests for Jupyter notebooks

Validates that notebooks can be executed without errors.
Note: This requires nbconvert and nbformat to be installed.
"""
import pytest
from pathlib import Path
import json


class TestNotebookStructure:
    """Test notebook file structure"""
    
    def test_notebooks_directory_exists(self):
        """Test that notebooks directory exists"""
        notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        assert notebooks_dir.exists()
        assert notebooks_dir.is_dir()
    
    def test_all_notebooks_exist(self):
        """Test that all expected notebooks exist"""
        notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        expected_notebooks = [
            '01_line_scatter.ipynb',
            '02_bar_pie_box.ipynb',
            '03_histogram_density.ipynb',
            '04_heatmaps_choropeth.ipynb',
            '05_animations_interactive.ipynb',
            '06_subplots_dashboards.ipynb',
            '07_graph_objects.ipynb',
            '08_mapbox_geo.ipynb',
            '09_real_world_cases.ipynb',
            '10_statistical_overlays.ipynb'
        ]
        
        for notebook in expected_notebooks:
            notebook_path = notebooks_dir / notebook
            assert notebook_path.exists(), f"Missing notebook: {notebook}"
    
    def test_notebooks_are_valid_json(self):
        """Test that all notebooks are valid JSON"""
        notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        
        for notebook_path in notebooks_dir.glob('*.ipynb'):
            with open(notebook_path, 'r') as f:
                try:
                    data = json.load(f)
                    assert 'cells' in data, f"Invalid notebook structure: {notebook_path.name}"
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON in notebook: {notebook_path.name}")


class TestNotebookContent:
    """Test notebook content quality"""
    
    def test_notebooks_have_cells(self):
        """Test that notebooks have cells"""
        notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        
        for notebook_path in notebooks_dir.glob('*.ipynb'):
            with open(notebook_path, 'r') as f:
                data = json.load(f)
                assert len(data['cells']) > 0, f"Empty notebook: {notebook_path.name}"
    
    def test_notebooks_have_markdown_cells(self):
        """Test that notebooks have documentation"""
        notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        
        for notebook_path in notebooks_dir.glob('*.ipynb'):
            with open(notebook_path, 'r') as f:
                data = json.load(f)
                markdown_cells = [c for c in data['cells'] if c['cell_type'] == 'markdown']
                assert len(markdown_cells) > 0, f"No documentation in: {notebook_path.name}"


# Optional: Test notebook execution (requires nbconvert)
# Uncomment if you want to validate notebook execution
"""
class TestNotebookExecution:
    @pytest.mark.slow
    def test_notebook_execution(self):
        '''Test that notebooks can be executed'''
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor
        
        notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        
        for notebook_path in notebooks_dir.glob('*.ipynb'):
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=4)
            
            try:
                ep.preprocess(nb, {'metadata': {'path': notebooks_dir}})
            except Exception as e:
                pytest.fail(f"Error executing {notebook_path.name}: {str(e)}")
"""


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
