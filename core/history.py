import os
import json
from pathlib import Path
from config import RESULTS_DIR, HISTORY_MAX_ITEMS

class HistoryManager:
    def __init__(self, ui):
        self.ui = ui
        self.files = []

    def load_history_list(self):
        self.ui.history_list.delete(0, "end")
        path = Path(RESULTS_DIR)
        path.mkdir(exist_ok=True)

        files = sorted(path.glob("*.json"), key=os.path.getmtime, reverse=True)
        files = files[:HISTORY_MAX_ITEMS]

        self.files = files
        for f in files:
            self.ui.history_list.insert("end", f.name)

    def on_history_selected(self, event=None):
        sel = self.ui.history_list.curselection()
        if not sel:
            return
        idx = sel[0]
        file_path = self.files[idx]

        with file_path.open() as f:
            data = json.load(f)

        # JSON view on the right
        self.ui.history_text.config(state="normal")
        self.ui.history_text.delete("1.0", "end")
        self.ui.history_text.insert("end", json.dumps(data, indent=2))
        self.ui.history_text.config(state="disabled")

        # Repopulate central block with colors & data
        self.ui.populate_run_into_central(data)
