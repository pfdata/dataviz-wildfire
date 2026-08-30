from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
BMEL_DIR = DATA_DIR / "bmel-statistik_de"
DWD_DIR = DATA_DIR / "dwd"
CMIP6_DIR = DATA_DIR / "cmip6"
