"""Standalone launcher for the LakeShore 335 app.

Run from this repository with ``python app.py``, or from bl18c_controller
with ``python apps/LakeShore335/app.py``. The local package registration
keeps relative imports working both in a separate checkout and as a submodule.
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import sys

from PyQt6.QtWidgets import QApplication


_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG_NAME = "_lakeshore335_standalone"

if _PKG_NAME not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        _PKG_NAME, os.path.join(_HERE, "__init__.py"),
        submodule_search_locations=[_HERE],
    )
    _pkg = importlib.util.module_from_spec(_spec)
    sys.modules[_PKG_NAME] = _pkg
    _spec.loader.exec_module(_pkg)

LakeShore335Window = importlib.import_module(
    f"{_PKG_NAME}.lakeshore335_app"
).LakeShore335Window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LakeShore335Window()
    window.show()
    sys.exit(app.exec())
