"""Run the whole pipeline: build data -> evaluate models -> leakage check."""
import subprocess
import sys
from pathlib import Path

src = Path(__file__).resolve().parent / "src"
for script in ("build_dataset.py", "evaluate.py", "leakage_check.py"):
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, script], cwd=src, check=True)
