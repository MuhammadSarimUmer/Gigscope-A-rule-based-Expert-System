"""Knowledge base integrity via validate_kb."""

import subprocess
import sys
from pathlib import Path


def test_validate_kb_passes():
    root = Path(__file__).resolve().parent.parent
    proc = subprocess.run(
        [sys.executable, str(root / "validate_kb.py")],
        capture_output=True,
        text=True,
        cwd=str(root),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
