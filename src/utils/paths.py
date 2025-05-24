from pathlib import Path
import sys

# Root
ROOT_DIR = Path(__file__).resolve().parents[2]

# Directories
DATA_DIR = ROOT_DIR / "data"

# Adding external lib from Plaxis to path
external_libs_path = f"{ROOT_DIR}\\src\\plaxis\\external_libs"
sys.path.append(str(external_libs_path))