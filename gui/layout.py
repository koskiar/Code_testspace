import tkinter as tk
from tkinter import ttk
from config import APP_TITLE
from core.runner import Runner
from core.history import HistoryManager
from gui.styles import apply_styles
from gui.test_builder_panel import TestBuilderPanel
from gui.sequence_builder_panel import SequenceBuilderPanel


class MainUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)

        # Dark mode state
        self.dark_mode = tk.BooleanVar(value=False)

        # Fullscreen on Raspberry Pi
        try:
            self.root.attributes("-zoomed", True)
        except Exception:
            self.root.state("zoomed")

        apply_styles(self.root, dark_mode=self.dark_mode.get())

        self.runner = Runner(self)
        self.history = HistoryManager(self)

        self._scan_active = False  # UI flag for live scan button

        self._build_layout()
        self.runner.load_definitions()
        self.history.load_history_list()

    # ------------------------------------------------------------
    # MAIN LAYOUT
    # ------------------------------------------------------------
    def _build_layout(self):
        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=1)

        # ---------------- HEADER ----------------
        header_outer = ttk.Frame(self.root, style="Header.TFrame", padding=(15, 10))
        header_outer.grid(row=0, column=0, columnspan=2, sticky="nsew")
        header_outer.columnconfigure(0, weight=1)

        header = ttk.Frame(header_outer, style="HeaderInner.TFrame", padding=(10, 8))
        header.grid(row=0, column=0, sticky="nsew")

        for i in range(12):
            header.columnconfigure(i, weight=0)
        header.columnconfigure(11, weight=1)

        ttk.Label(header, text="Tester", style="Header.TLabel").grid(row=0, column=0, padx=(0, 5))
        self.tester_var = tk.StringVar()
        ttk.Entry(header, textvariable=self.tester_var, width=18).grid(row=0, column=1, padx=(0, 20))

        ttk.Label(header, text="Board ID", style="Header.TLabel").grid(row=0, column=2, padx=(0, 5))
        self.board_var = tk.StringVar()
        ttk.Entry(header, textvariable=self.board_var, width=18).grid(row=0, column=3, padx=(0, 20))

        self.start_button = ttk.Button(
            header,
            text="Start Test Sequence",
            style="Header.TButton",
            command=self.runner.start_sequence
        )
        self.start_button.grid(row=0, column=4, padx=(10, 10))

        # Continue on Fail checkbox
        self.continue_on_fail = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            header,
            text="Continue on Fail",
            variable=self.continue_on_fail
        ).grid(row=0, column=5, padx=(10, 0))

        # Dark mode toggle
        ttk.Checkbutton(
            header,
            text="Dark Mode",
            variable=self.dark_mode,
            command=self._toggle_dark_mode
        ).grid(row=0, column=6, padx=(10, 0))

        # Connection / status indicator
        self.conn_var = tk.StringVar(value="Status: Idle")
        ttk.Label(header, textvariable=self.conn_var, style="Header.TLabel").grid(row=0, column=7, padx=(10, 0))

        # ---------------- LEFT / RIGHT PANELS ----------------
        left = ttk.Frame(self.root, style="Main.TFrame", padding=(15, 10))
        left.grid(row=1, column=0, sticky="nsew")
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        right = ttk.Frame(self.root, style="Main.TFrame", padding=(5, 10))
        right.grid(row=1, column=1, sticky="nsew")
        right.rowconfigure(2, weight=1)
        right.columnconfigure(0, weight=1)

        self._build_left_panel(left)
        self._build_right_panel(right)
        self._build_status_bar()

    # ------------------------------------------------------------
    # LEFT PANEL (SEQUENCES + TEST EXECUTION)
    # ------------------------------------------------------------
    def _build_left_panel(self, parent):
        # Sequence selector
        seq_frame = ttk.LabelFrame(
            parent,
            text="Available Test Sequences",
            style="Sequence.TLabelframe",
            padding=(10, 8)
        )
        seq_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        seq_frame.columnconfigure(0, weight=1)

        self.sequence_var = tk.StringVar()
        self.sequence_combo = ttk.Combobox(
            seq_frame,
            textvariable=self.sequence_var,
            state="readonly",
            width=40
        )
        self.sequence_combo.grid(row=0, column=0, sticky="w")
        self.sequence_combo.bind("<<ComboboxSelected>>", self.runner.on_sequence_selected)

        # Central execution block
        central_outer = ttk.Frame(parent, style="CentralBlock.TFrame", padding=(15, 15))
        central_outer.grid(row=1, column=0, sticky="nsew")
        central_outer.rowconfigure(1, weight=1)
        central_outer.columnconfigure(0, weight=1)

        ttk.Label(
            central_outer,
            text="Test Execution",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Treeview
        columns = ("name", "status", "duration", "result")
        self.tests_tree = ttk.Treeview(
            central_outer,
            columns=columns,
            show="tree headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        self.tests_tree.heading("#0", text="#")
        self.tests_tree.heading("name", text="Test / Subtest")
        self.tests_tree.heading("status", text="Status")
        self.tests_tree.heading("duration", text="Duration")
        self.tests_tree.heading("result", text="Result")

        for col in ("#0", "name", "status", "duration", "result"):
            self.tests_tree.column(col, stretch=True)

        self.tests_tree.grid(row=1, column=0, sticky="nsew", pady=(5, 5))

        scrollbar = ttk.Scrollbar(central_outer, orient="vertical", command=self.tests_tree.yview)
        self.tests_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns", padx=(5, 0))

        # Row color tags
        self._configure_row_tags()

        # Expand/collapse behavior with gentle animation
        self.tests_tree.bind("<Double-1>", self._toggle_expand)

        # Per-test progress bar
        self.test_progress = ttk.Progressbar(
            central_outer,
            mode="determinate",
            length=350
        )
        self.test_progress.grid(row=2, column=0, sticky="w", pady=(8, 0))

        # Summary card
        self.summary_frame = ttk.Frame(parent, padding=10, style="CentralBlock.TFrame")
        self.summary_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.summary_frame.columnconfigure(0, weight=1)

        self.summary_text = tk.Text(self.summary_frame, height=6, wrap="word")
        self.summary_text.grid(row=0, column=0, sticky="ew")

        self.run_remaining_button = ttk.Button(
            self.summary_frame,
            text="Run Remaining Tests",
            command=self.run_remaining_tests_clicked
        )
        self.run_remaining_button.grid(row=1, column=0, sticky="w", pady=(5, 0))

        self.summary_frame.grid_remove()

        self._style_text_widget(self.summary_text)

    # ------------------------------------------------------------
    # RIGHT PANEL (HISTORY + BLUETOOTH + TEST BUILDER)
    # ------------------------------------------------------------
    def _build_right_panel(self, parent):
        # History list (top)
        hist_frame = ttk.LabelFrame(
            parent,
            text="Test History",
            style="History.TLabelframe",
            padding=(10, 8)
        )
        hist_frame.grid(row=0, column=0, sticky="nsew")
        hist_frame.rowconfigure(0, weight=1)
        hist_frame.columnconfigure(0, weight=1)

        self.history_list = tk.Listbox(hist_frame, height=8)
        self.history_list.grid(row=0, column=0, sticky="ew")
        self.history_list.bind("<<ListboxSelect>>", self.history.on_history_selected)

        self.history_list.bind("<Enter>", lambda e: self.history_list.config(cursor="hand2"))
        self.history_list.bind("<Leave>", lambda e: self.history_list.config(cursor=""))

        # Bluetooth live scanner (middle)
        bt_frame = ttk.LabelFrame(
            parent,
            text="Bluetooth Devices (Live Scan)",
            style="History.TLabelframe",
            padding=(10, 8)
        )
        bt_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        bt_frame.rowconfigure(0, weight=1)
        bt_frame.columnconfigure(0, weight=1)

        self.bt_list = tk.Listbox(bt_frame, height=12)
        self.bt_list.grid(row=0, column=0, sticky="nsew")
        self.bt_list.bind("<Double-Button-1>", lambda e: self._connect_to_selected_bt_device())

        self.bt_connect_button = ttk.Button(
            bt_frame,
            text="Connect to Selected",
            command=self._connect_to_selected_bt_device
        )
        self.bt_connect_button.grid(row=1, column=0, sticky="w", pady=(5, 0))

        self.bt_scan_button = ttk.Button(
            bt_frame,
            text="Start Live Scan",
            command=self._toggle_live_scan
        )
        self.bt_scan_button.grid(row=2, column=0, sticky="w", pady=(5, 0))

        self._style_bt_list()

        # ---------- Test Builder panel (bottom) ----------
        builder_frame = TestBuilderPanel(parent, self)
        builder_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        # ---------- Sequence Builder panel ----------
        seq_builder = SequenceBuilderPanel(parent, self)
        seq_builder.grid(row=3, column=0, sticky="nsew", pady=(10, 0))


    # ------------------------------------------------------------
    # STATUS BAR
    # ------------------------------------------------------------
    def _build_status_bar(self):
        status_frame = ttk.Frame(self.root, padding=(10, 5))
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        status_frame.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style="Status.TLabel"
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        self.sequence_progress = ttk.Progressbar(
            status_frame,
            mode="determinate",
            length=220
        )
        self.sequence_progress.grid(row=0, column=1, sticky="e", padx=(10, 0))

    # ------------------------------------------------------------
    # UI HELPERS CALLED BY RUNNER
    # ------------------------------------------------------------
    def set_status(self, text: str):
        self.status_var.set(text)
        self.root.update_idletasks()

    def set_sequence_progress(self, value: float):
        self.sequence_progress["value"] = value
        self.root.update_idletasks()

    def set_test_progress(self, value: float):
        self.test_progress["value"] = value
        self.root.update_idletasks()

    def clear_tests_tree(self):
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)

    # Summary card controls
    def show_summary_card(self, run_record, stopped_early):
        self.summary_frame.grid()
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", "end")

        if stopped_early:
            self.summary_text.insert("end", "Sequence stopped early due to failure.\n\n")
            self.summary_text.insert("end", "Remaining tests were not run.\n\n")
        else:
            self.summary_text.insert("end", "Sequence completed.\n\n")

        self.summary_text.insert("end", f"Overall Result: {run_record['overall_result']}\n")
        self.summary_text.insert("end", f"Duration: {run_record['duration_seconds']:.1f}s\n\n")

        for t in run_record["tests"]:
            self.summary_text.insert("end", f"{t['name']}: {t['result']}\n")

        self.summary_text.config(state="disabled")

    def hide_summary_card(self):
        self.summary_frame.grid_remove()

    def run_remaining_tests_clicked(self):
        self.runner.run_remaining_tests()

    # History repopulation (with staggered highlight on tests)
    def populate_run_into_central(self, run_record: dict):
        self.clear_tests_tree()
        tests = run_record.get("tests", [])

        parent_ids = []
        for idx, t in enumerate(tests, start=1):
            test_name = t["name"]
            overall = t["result"]
            duration = f'{t.get("duration_seconds", 0):.1f}s'
            status = "Done"

            parent_id = self.tests_tree.insert(
                "",
                "end",
                iid=test_name,
                text=str(idx),
                values=(test_name, status, duration, overall),
            )

            tag = "passed" if overall == "PASS" else "failed"
            self.tests_tree.item(parent_id, tags=(tag,))
            parent_ids.append((parent_id, t))

        # Animate tests (slow, visible)
        self._animate_rows([pid for pid, _ in parent_ids], base_delay=80)

        # Insert subtests with alternating shading
        for parent_id, t in parent_ids:
            subtests = t.get("subtests", [])
            for i, sub in enumerate(subtests):
                reading = f'{sub["reading"]} {sub.get("units", "")}'.strip()
                tag = "sub_even" if i % 2 == 0 else "sub_odd"
                self.tests_tree.insert(
                    parent_id,
                    "end",
                    text="",
                    values=(sub["name"], "", "", f'{sub["result"]} ({reading})'),
                    tags=(tag,)
                )

    # ------------------------------------------------------------
    # BLUETOOTH UI HELPERS
    # ------------------------------------------------------------
    def _rssi_to_bars(self, rssi: int) -> str:
        if rssi is None:
            return "⬜⬜⬜⬜⬜"
        if rssi >= -50:
            return "🟩🟩🟩🟩🟩"
        if rssi >= -60:
            return "🟩🟩🟩🟩⬜"
        if rssi >= -70:
            return "🟩🟩🟩⬜⬜"
        if rssi >= -80:
            return "🟩🟩⬜⬜⬜"
        return "🟩⬜⬜⬜⬜"

    def show_bluetooth_results(self, devices):
        self.bt_list.delete(0, "end")
        if not devices:
            self.bt_list.insert("end", "No Bluetooth devices found.")
            return

        for d in devices:
            bars = self._rssi_to_bars(d["rssi"])
            label = f"{bars}  {d['name'] or 'Unknown'} — {d['address']}  (RSSI {d['rssi']} dBm)"
            if d.get("is_target"):
                label = "[TARGET] " + label
            self.bt_list.insert("end", label)

    def show_bluetooth_connection_result(self, address: str, success: bool):
        if success:
            self.conn_var.set(f"Connected to {address}")
        else:
            self.conn_var.set(f"Failed to connect to {address}")

    def _connect_to_selected_bt_device(self):
        selection = self.bt_list.curselection()
        if not selection:
            self.set_status("No Bluetooth device selected.")
            return

        line = self.bt_list.get(selection[0])
        if "—" not in line:
            self.set_status("Could not parse selected device address.")
            return

        try:
            address_part = line.split("—", 1)[1].strip()
            address = address_part.split("  ", 1)[0].strip()
        except Exception:
            self.set_status("Could not parse selected device address.")
            return

        self.runner.connect_to_selected_device(address)

    def _toggle_live_scan(self):
        if not self._scan_active:
            self._scan_active = True
            self.bt_scan_button.config(text="Stop Live Scan")
            self.runner.start_continuous_scan()
            self.set_status("Starting live Bluetooth scan...")
        else:
            self._scan_active = False
            self.bt_scan_button.config(text="Start Live Scan")
            self.runner.stop_continuous_scan()
            self.set_status("Live Bluetooth scan stopped.")

    # ------------------------------------------------------------
    # DARK MODE TOGGLE + TEXT/LIST STYLING
    # ------------------------------------------------------------
    def _toggle_dark_mode(self):
        apply_styles(self.root, dark_mode=self.dark_mode.get())
        self._style_text_widget(self.summary_text)
        self._style_bt_list()
        self._configure_row_tags()

        if self.dark_mode.get():
            self.history_list.config(
                bg="#2a2c31",
                fg="#f5f5f5",
                selectbackground="#0078d7",
                selectforeground="#ffffff",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            self.history_list.config(
                bg="#ffffff",
                fg="#222222",
                selectbackground="#0078d7",
                selectforeground="#ffffff",
                borderwidth=0,
                highlightthickness=0
            )

    def _style_text_widget(self, widget: tk.Text):
        if self.dark_mode.get():
            widget.config(
                bg="#2a2c31",
                fg="#f5f5f5",
                insertbackground="#f5f5f5",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            widget.config(
                bg="#ffffff",
                fg="#222222",
                insertbackground="#222222",
                borderwidth=0,
                highlightthickness=0
            )

    def _style_bt_list(self):
        if self.dark_mode.get():
            self.bt_list.config(
                bg="#2a2c31",
                fg="#f5f5f5",
                selectbackground="#0078d7",
                selectforeground="#ffffff",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            self.bt_list.config(
                bg="#ffffff",
                fg="#222222",
                selectbackground="#0078d7",
                selectforeground="#ffffff",
                borderwidth=0,
                highlightthickness=0
            )
    def _style_listbox(self, lb: tk.Listbox):
        if self.dark_mode.get():
            lb.config(
                bg="#2a2c31",
                fg="#f5f5f5",
                selectbackground="#0078d7",
                selectforeground="#ffffff",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            lb.config(
                bg="#ffffff",
                fg="#222222",
                selectbackground="#0078d7",
                selectforeground="#ffffff",
                borderwidth=0,
                highlightthickness=0
            )
        

    def _configure_row_tags(self):
        if self.dark_mode.get():
            sub_bg_even = "#3a3c42"
            sub_bg_odd = "#34363c"
        else:
            sub_bg_even = "#f7f7f7"
            sub_bg_odd = "#ffffff"

        self.tests_tree.tag_configure("notrun", background="#d9d9d9")
        self.tests_tree.tag_configure("running", background="#fff3cd")
        self.tests_tree.tag_configure("passed", background="#d4edda")
        self.tests_tree.tag_configure("failed", background="#f8d7da")
        self.tests_tree.tag_configure("sub_even", background=sub_bg_even)
        self.tests_tree.tag_configure("sub_odd", background=sub_bg_odd)

    def _toggle_expand(self, event):
        item = self.tests_tree.identify_row(event.y)
        if not item:
            return
        if not self.tests_tree.get_children(item):
            return

        is_open = self.tests_tree.item(item, "open")
        self.tests_tree.item(item, open=not is_open)

        if not is_open:
            children = list(self.tests_tree.get_children(item))
            self._animate_rows(children, base_delay=80)

    def _animate_rows(self, items, base_delay=80):
        for i, iid in enumerate(items):
            self.root.after(base_delay * i, lambda row=iid: self._flash_row(row))

    def _flash_row(self, iid):
        original_tags = self.tests_tree.item(iid, "tags")
        self.tests_tree.item(iid, tags=original_tags + ("running",))
        self.root.after(180, lambda: self.tests_tree.item(iid, tags=original_tags))

