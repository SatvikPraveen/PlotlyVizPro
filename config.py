"""
Configuration Management for PlotlyVizPro

Loads settings from environment variables or uses sensible defaults.
"""
import os
from pathlib import Path
from typing import Optional


class Config:
    """Central configuration class"""

    # Project root directory
    BASE_DIR = Path(__file__).parent.absolute()

    # ========================================
    # Environment Settings
    # ========================================
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

    # ========================================
    # API Keys
    # ========================================
    MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN', '')

    # ========================================
    # Directory Paths
    # ========================================
    DATASETS_DIR = BASE_DIR / os.getenv('DATASETS_DIR', 'datasets')
    EXPORTS_DIR = BASE_DIR / 'exports'
    EXPORT_HTML_DIR = BASE_DIR / os.getenv('EXPORT_HTML_DIR', 'exports/html')
    EXPORT_IMAGES_DIR = BASE_DIR / os.getenv('EXPORT_IMAGES_DIR', 'exports/images')
    LOGS_DIR = BASE_DIR / 'logs'

    # ========================================
    # Server Configuration
    # ========================================
    JUPYTER_PORT = int(os.getenv('JUPYTER_PORT', 8888))
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))

    # ========================================
    # Plotting Defaults
    # ========================================
    DEFAULT_PLOTLY_TEMPLATE = os.getenv('DEFAULT_PLOTLY_TEMPLATE', 'plotly_white')
    DEFAULT_FIGURE_WIDTH = int(os.getenv('DEFAULT_FIGURE_WIDTH', 1200))
    DEFAULT_FIGURE_HEIGHT = int(os.getenv('DEFAULT_FIGURE_HEIGHT', 600))
    EXPORT_DPI = int(os.getenv('EXPORT_DPI', 300))

    # ========================================
    # Data Generation
    # ========================================
    RANDOM_SEED = int(os.getenv('RANDOM_SEED', 42))
    DATASET_SIZE = int(os.getenv('DATASET_SIZE', 1000))

    # ========================================
    # Performance Settings
    # ========================================
    MAX_PLOT_ROWS = int(os.getenv('MAX_PLOT_ROWS', 50000))
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 3600))

    # ========================================
    # Logging
    # ========================================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = BASE_DIR / os.getenv('LOG_FILE', 'logs/plotlyvizpro.log')

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        for directory in [
            cls.DATASETS_DIR,
            cls.EXPORTS_DIR,
            cls.EXPORT_HTML_DIR,
            cls.EXPORT_IMAGES_DIR,
            cls.LOGS_DIR
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_mapbox_token(cls) -> Optional[str]:
        """Get Mapbox token with validation"""
        token = cls.MAPBOX_TOKEN
        if not token or token == 'your_mapbox_token_here':
            return None
        return token

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode"""
        return cls.ENVIRONMENT == 'development'

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode"""
        return cls.ENVIRONMENT == 'production'

    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)"""
        print("=" * 50)
        print("PlotlyVizPro Configuration")
        print("=" * 50)
        print(f"Environment: {cls.ENVIRONMENT}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Base Directory: {cls.BASE_DIR}")
        print(f"Datasets Directory: {cls.DATASETS_DIR}")
        print(f"Exports Directory: {cls.EXPORTS_DIR}")
        print(f"Jupyter Port: {cls.JUPYTER_PORT}")
        print(f"Streamlit Port: {cls.STREAMLIT_PORT}")
        print(f"Mapbox Token: {'Set' if cls.get_mapbox_token() else 'Not Set'}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print("=" * 50)


class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    ENVIRONMENT = 'development'


class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    ENVIRONMENT = 'production'


class TestingConfig(Config):
    """Testing-specific configuration"""
    DEBUG = True
    ENVIRONMENT = 'testing'
    # Use temporary directories for testing
    DATASETS_DIR = Path('/tmp/plotlyvizpro/datasets')
    EXPORTS_DIR = Path('/tmp/plotlyvizpro/exports')


def get_config() -> Config:
    """
    Get configuration based on ENVIRONMENT variable

    Returns:
        Config: Configuration object for current environment
    """
    env = os.getenv('ENVIRONMENT', 'development')

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }

    config_class = config_map.get(env, Config)
    return config_class


# Create default config instance
config = get_config()

# Ensure directories exist
config.ensure_directories()


if __name__ == '__main__':
    # Print configuration when run directly
    config.print_config()
