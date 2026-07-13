"""
Pytest configuration for the backend test suite.

Ensures the backend package root (this directory) is importable so tests can
`from app.services... import ...` regardless of the working directory pytest is
invoked from (e.g. `python -m pytest backend/tests/` at the repo root in CI).
"""
import os
import sys

_BACKEND_ROOT = os.path.dirname(os.path.abspath(__file__))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)
