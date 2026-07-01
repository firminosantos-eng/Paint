"""
Atalho para rodar o projeto a partir da raiz do repositório, sem precisar
configurar o PYTHONPATH manualmente.

Uso:
    python executar.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from paint.main import main

if __name__ == "__main__":
    main()
