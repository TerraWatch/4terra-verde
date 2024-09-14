import os

# Path settings
class PathConfig:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
    PROCESSED_DATA_FILE_PATH = os.path.join(DATA_DIR, 'processed')


# Main config class that combines all configurations
class Config:
    PATHS = PathConfig
