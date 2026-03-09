"""
Tests for Streamlit application

Validates that Streamlit app and pages can be imported.
"""
import pytest
from pathlib import Path
import sys
import importlib.util


class TestStreamlitApp:
    """Test Streamlit application structure"""
    
    def test_app_file_exists(self):
        """Test that main app.py exists"""
        app_path = Path(__file__).parent.parent / 'app.py'
        assert app_path.exists()
    
    def test_app_can_be_imported(self):
        """Test that app.py can be imported without errors"""
        app_path = Path(__file__).parent.parent / 'app.py'
        spec = importlib.util.spec_from_file_location("app", app_path)
        module = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(module)
        except ImportError as e:
            # Streamlit import errors are OK in test environment
            if 'streamlit' not in str(e):
                raise


class TestStreamlitPages:
    """Test Streamlit pages"""
    
    def test_pages_directory_exists(self):
        """Test that pages directory exists"""
        pages_dir = Path(__file__).parent.parent / 'pages'
        assert pages_dir.exists()
        assert pages_dir.is_dir()
    
    def test_all_pages_exist(self):
        """Test that all expected pages exist"""
        pages_dir = Path(__file__).parent.parent / 'pages'
        expected_pages = [
            'notebook_01.py',
            'notebook_02.py',
            'notebook_03.py',
            'notebook_04.py',
            'notebook_05.py',
            'notebook_06.py',
            'notebook_07.py',
            'notebook_08.py',
            'notebook_09.py',
            'notebook_10.py'
        ]
        
        for page in expected_pages:
            page_path = pages_dir / page
            assert page_path.exists(), f"Missing page: {page}"
    
    def test_pages_are_valid_python(self):
        """Test that all pages are valid Python files"""
        pages_dir = Path(__file__).parent.parent / 'pages'
        
        for page_path in pages_dir.glob('*.py'):
            # Try to compile the file to check syntax
            with open(page_path, 'r') as f:
                try:
                    compile(f.read(), page_path.name, 'exec')
                except SyntaxError:
                    pytest.fail(f"Syntax error in: {page_path.name}")


class TestUtilities:
    """Test utility modules"""
    
    def test_utils_directory_exists(self):
        """Test that utils directory exists"""
        utils_dir = Path(__file__).parent.parent / 'utils'
        assert utils_dir.exists()
        assert utils_dir.is_dir()
    
    def test_plot_utils_exists(self):
        """Test that plot_utils.py exists"""
        plot_utils_path = Path(__file__).parent.parent / 'utils' / 'plot_utils.py'
        assert plot_utils_path.exists()
    
    def test_streamlit_utils_exists(self):
        """Test that streamlit_utils.py exists"""
        streamlit_utils_path = Path(__file__).parent.parent / 'utils' / 'streamlit_utils.py'
        assert streamlit_utils_path.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
