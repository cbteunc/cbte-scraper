import sys
from pathlib import Path

# Configura el acceso a módulos del directorio inmediatamente superior
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))