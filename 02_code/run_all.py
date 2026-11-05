"""
run_all.py -- runs the whole analysis in the right order.

    python 02_code/run_all.py

Order: 01 data -> 02 replication -> 03 update -> 04 power & bias -> 05 meta-regression.
After new studies were added to 01_data/update_studies.csv, simply run this again.
"""

import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
SCRIPTS = ["01_prepare_data.py", "02_replication.py", "03_update.py",
           "04_power_bias.py", "05_meta_regression.py"]

for script in SCRIPTS:
    print(f"\n{'=' * 78}\n{script}\n{'=' * 78}")
    result = subprocess.run([sys.executable, str(CODE / script)], cwd=CODE.parent)
    if result.returncode != 0:
        sys.exit(f"\n{script} failed -- stopped here.")
print("\nall done. Tables: 04_report/tables/, figures: 04_report/figures/")
