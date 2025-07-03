from pathlib import Path

from .app import PyRigApp

HERE = Path(__file__).parent
REPO = HERE.parent

PyRigApp.run_cmdline()
