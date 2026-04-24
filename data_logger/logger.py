import json
from pathlib import Path
from datetime import datetime
from config import RESULTS_DIR

def save_run_result(run_record: dict):
    Path(RESULTS_DIR).mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fname = f"{ts}_{run_record['sequence_name'].replace(' ', '_')}.json"
    path = Path(RESULTS_DIR) / fname
    with path.open("w") as f:
        json.dump(run_record, f, indent=2)
