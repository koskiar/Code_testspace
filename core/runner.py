import json
import time
import threading
import queue
import importlib
import threading
import asyncio
from pathlib import Path
from config import TEST_DEFINITION_FILE, DEFAULT_TIMEOUT
from data_logger.logger import save_run_result
from core.bluetooth_manager import BluetoothManager


class Runner:
    def __init__(self, ui):
        self.ui = ui
        self.defs = {}
        self.current_sequence = None
        self.stop_flag = False
        self.remaining_tests = []  # for “Run Remaining Tests”
        # Bluetooth manager: adjust prefix to match your board name
        self.bt = BluetoothManager(target_name_prefix="TEST_BOARD")
        # Continuous scan flag
        self._scan_running = False

    # ------------------------------------------------------------
    # LOAD TEST DEFINITIONS
    # ------------------------------------------------------------
    def load_definitions(self):
        path = Path(TEST_DEFINITION_FILE)
        with path.open() as f:
            self.defs = json.load(f)

        seq_names = [s["name"] for s in self.defs["sequences"]]
        self.ui.sequence_combo["values"] = seq_names

        if seq_names:
            self.ui.sequence_combo.current(0)
            self.on_sequence_selected()

    # ------------------------------------------------------------
    # WHEN USER SELECTS A TEST SEQUENCE
    # ------------------------------------------------------------
    def on_sequence_selected(self, event=None):
        name = self.ui.sequence_var.get()

        if not name and self.ui.sequence_combo["values"]:
            name = self.ui.sequence_combo["values"][0]
            self.ui.sequence_var.set(name)

        self.current_sequence = next(
            (s for s in self.defs["sequences"] if s["name"] == name),
            None
        )

        self._populate_tests_tree()
        self.ui.hide_summary_card()

    # ------------------------------------------------------------
    # POPULATE CENTRAL BLOCK WITH TESTS + SUBTESTS
    # ------------------------------------------------------------
    def _populate_tests_tree(self):
        tree = self.ui.tests_tree
        self.ui.clear_tests_tree()

        if not self.current_sequence:
            return

        for idx, test_name in enumerate(self.current_sequence["tests"], start=1):
            test_def = self.defs["tests"][test_name]

            parent_id = tree.insert(
                "",
                "end",
                iid=test_name,
                text=str(idx),
                values=(test_name, "Not run", "--", "Not run"),
                tags=("notrun",)
            )

            for sub in test_def["subtests"]:
                tree.insert(
                    parent_id,
                    "end",
                    text="",
                    values=(sub["name"], "", "", f'Cond: {sub["condition"]}'),
                    tags=("subtest",)
                )

    # ------------------------------------------------------------
    # START FULL SEQUENCE
    # ------------------------------------------------------------
    def start_sequence(self):
        tester = self.ui.tester_var.get().strip()
        board = self.ui.board_var.get().strip()

        if not tester or not board:
            self.ui.set_status("Enter Tester and Board ID before starting.")
            return

        if not self.current_sequence:
            self.ui.set_status("No sequence selected.")
            return

        self.ui.hide_summary_card()
        self.remaining_tests = []  # reset

        thread = threading.Thread(
            target=self._run_sequence_thread,
            args=(tester, board, None),
            daemon=True
        )
        thread.start()

    # ------------------------------------------------------------
    # RUN REMAINING TESTS ONLY
    # ------------------------------------------------------------
    def run_remaining_tests(self):
        tester = self.ui.tester_var.get().strip()
        board = self.ui.board_var.get().strip()

        if not self.remaining_tests:
            self.ui.set_status("No remaining tests to run.")
            return

        self.ui.hide_summary_card()

        thread = threading.Thread(
            target=self._run_sequence_thread,
            args=(tester, board, self.remaining_tests),
            daemon=True
        )
        thread.start()

    # ------------------------------------------------------------
    # MAIN TEST EXECUTION THREAD
    # ------------------------------------------------------------
    def _run_sequence_thread(self, tester, board, override_tests):
        self.stop_flag = False

        if override_tests is None:
            tests = self.current_sequence["tests"]
        else:
            tests = override_tests

        total_tests = len(tests)
        seq_name = self.current_sequence["name"]

        run_record = {
            "tester": tester,
            "board_id": board,
            "sequence_name": seq_name,
            "time_started": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "tests": []
        }

        stopped_early = False

        for idx, test_name in enumerate(tests, start=1):
            if self.stop_flag:
                break

            self.ui.set_status(f"Running test {idx}/{total_tests} — {test_name}")
            self.ui.set_sequence_progress((idx - 1) / total_tests * 100)
            self.ui.set_test_progress(0)

            self._update_test_row_status(
                test_name,
                status="Running",
                duration="--",
                result="Running",
                tag="running"
            )

            test_def = self.defs["tests"][test_name]
            module_name = test_def["module"]
            timeout = test_def.get("timeout", DEFAULT_TIMEOUT)

            result_queue = queue.Queue()

            def worker():
                try:
                    mod = importlib.import_module(f"gpio_test.{module_name}")
                    res = mod.run(test_def)
                    result_queue.put(("success", res))
                except Exception as e:
                    result_queue.put(("error", str(e)))

            t = threading.Thread(target=worker, daemon=True)
            t.start()

            start_time = time.time()
            finished = False
            status = "error"
            payload = None

            while True:
                elapsed = time.time() - start_time
                remaining = timeout - elapsed

                self.ui.set_test_progress((elapsed / timeout) * 100)

                if remaining <= 0:
                    break

                try:
                    status, payload = result_queue.get_nowait()
                    finished = True
                    break
                except queue.Empty:
                    time.sleep(0.1)

            duration = time.time() - start_time

            # ------------------------------------------------------------
            # HANDLE RESULT
            # ------------------------------------------------------------
            if not finished:
                test_result = {
                    "name": test_name,
                    "time_started": "",
                    "time_ended": "",
                    "duration_seconds": duration,
                    "result": "FAIL",
                    "subtests": []
                }

                self._update_test_row_status(
                    test_name,
                    status="Timed out",
                    duration=f"{duration:.1f}s",
                    result="FAIL",
                    tag="failed"
                )

            else:
                test_result = payload
                test_result["duration_seconds"] = duration
                overall = test_result["result"]

                tag = "passed" if overall == "PASS" else "failed"

                self._update_test_row_status(
                    test_name,
                    status="Done",
                    duration=f"{duration:.1f}s",
                    result=overall,
                    tag=tag
                )

                self._update_subtests_for(test_name, test_result["subtests"])

            run_record["tests"].append(test_result)

            # ------------------------------------------------------------
            # STOP ON FAIL (unless Continue on Fail is checked)
            # ------------------------------------------------------------
            if test_result["result"] == "FAIL" and not self.ui.continue_on_fail.get():
                stopped_early = True
                break

        # ------------------------------------------------------------
        # FINISH SEQUENCE
        # ------------------------------------------------------------
        run_record["time_ended"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        run_record["duration_seconds"] = sum(t["duration_seconds"] for t in run_record["tests"])
        run_record["overall_result"] = (
            "PASS" if all(t["result"] == "PASS" for t in run_record["tests"]) else "FAIL"
        )

        save_run_result(run_record)

        # Grey out remaining tests if stopped early
        if stopped_early:
            self.remaining_tests = tests[len(run_record["tests"]):]
            for tname in self.remaining_tests:
                self._update_test_row_status(
                    tname,
                    status="Not run",
                    duration="--",
                    result="Not run",
                    tag="notrun"
                )

            self.ui.set_status("Stopped early due to failure.")
            self.ui.show_summary_card(run_record, stopped_early=True)

        else:
            self.remaining_tests = []
            self.ui.set_status(f"Sequence '{seq_name}' complete: {run_record['overall_result']}")
            self.ui.show_summary_card(run_record, stopped_early=False)

        self.ui.set_sequence_progress(100)
        self.ui.set_test_progress(0)
        self.ui.history.load_history_list()

    # ------------------------------------------------------------
    # UPDATE MAIN TEST ROW
    # ------------------------------------------------------------
    def _update_test_row_status(self, test_name, status, duration, result, tag="notrun"):
        tree = self.ui.tests_tree

        if test_name not in tree.get_children():
            return

        index = tree.item(test_name, "text")
        name, _, _, _ = tree.item(test_name, "values")

        tree.item(
            test_name,
            text=index,
            values=(name, status, duration, result),
            tags=(tag,)
        )

        self.ui.root.update_idletasks()

    # ------------------------------------------------------------
    # UPDATE SUBTEST ROWS
    # ------------------------------------------------------------
    def _update_subtests_for(self, test_name, results):
        tree = self.ui.tests_tree

        if test_name not in tree.get_children():
            return

        for child in tree.get_children(test_name):
            tree.delete(child)

        for sub in results:
            reading = f'{sub["reading"]} {sub.get("units", "")}'.strip()
            res = sub["result"]

            tree.insert(
                test_name,
                "end",
                text="",
                values=(sub["name"], "", "", f'{res} ({reading})'),
                tags=("subtest",)
            )

    # ------------------------------------------------------------
    # BLUETOOTH INTEGRATION
    # ------------------------------------------------------------
    def scan_for_devices(self):
        """
        One-shot Bluetooth scan in a background thread (manual scan).
        """
        t = threading.Thread(target=self._scan_for_devices_worker, daemon=True)
        t.start()

    def _scan_for_devices_worker(self):
        self.ui.set_status("Scanning for Bluetooth devices...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            devices = loop.run_until_complete(self.bt.scan_devices(timeout=5))
        finally:
            loop.close()

        def update_ui():
            self.ui.show_bluetooth_results(devices)
            target_found = any(d["is_target"] for d in devices)
            if target_found:
                self.ui.set_status("Bluetooth scan complete — target device detected.")
            else:
                self.ui.set_status("Bluetooth scan complete — no target device found.")

        self.ui.root.after(0, update_ui)

    def start_continuous_scan(self):
        """
        Start a continuous BLE scan in a background thread (live scan).
        """
        if self._scan_running:
            return
        self._scan_running = True
        t = threading.Thread(target=self._continuous_scan_worker, daemon=True)
        t.start()

    def stop_continuous_scan(self):
        """
        Stop the continuous BLE scan.
        """
        self._scan_running = False

    def _continuous_scan_worker(self):
        """
        Worker loop that continuously scans and pushes results to the UI.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while self._scan_running:
            try:
                devices = loop.run_until_complete(self.bt.scan_devices(timeout=1))
            except Exception:
                devices = []

            self.ui.root.after(0, lambda d=devices: self.ui.show_bluetooth_results(d))

        loop.close()

    def connect_to_selected_device(self, address: str):
        """
        Connect to a selected device in a background thread.
        """
        t = threading.Thread(
            target=self._connect_to_selected_device_worker,
            args=(address,),
            daemon=True,
        )
        t.start()

    def _connect_to_selected_device_worker(self, address: str):
        self.ui.set_status(f"Connecting to {address}...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            ok = loop.run_until_complete(self.bt.connect_and_check(address))
        finally:
            loop.close()

        def update_ui():
            if ok:
                self.ui.set_status(f"Connected to {address}.")
                self.ui.show_bluetooth_connection_result(address, success=True)
            else:
                self.ui.set_status(f"Failed to connect to {address}.")
                self.ui.show_bluetooth_connection_result(address, success=False)

        self.ui.root.after(0, update_ui)
