from pathlib import Path
import os
import sys

try:
    # This will work when running as a script
    current_directory = Path(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    # This will work when running as an executable
    current_directory = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
PROJECT_NAME = "project_wild_fire"
PROJECT_PATH = current_directory.parents[0]

DATA_PATH = PROJECT_PATH.joinpath("data")
DOCS_PATH = PROJECT_PATH.joinpath("docs")
OUTPUT_PATH = PROJECT_PATH.joinpath("output")
SAMPLE_PATH = PROJECT_PATH.joinpath("sample")
DATA = PROJECT_PATH.joinpath("data")


BMEL = DATA_PATH.joinpath("bmel-statistik_de")
CMIP6 = DATA_PATH.joinpath("cmip6")
CLIMA_MODEL = DATA_PATH.joinpath("climate_model")
