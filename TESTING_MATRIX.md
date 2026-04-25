# Testing Matrix - Raspberry Pi Test Kit

## 📊 Comprehensive Test Coverage Map

Based on the Mermaid flowcharts, this matrix defines all test cases needed for complete coverage.

---

## 🔷 Test Case Format

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-001 | Core | Basic Test | Unit | System Ready | 1. Start app | Window opens | ☐ |

---

## 1️⃣ **Application Initialization Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-001 | GUI | Application Startup | Unit | main.py executable | 1. Run `python3 main.py` | Window appears, fully sized | ☐ |
| TC-002 | Styles | Light Mode Loads | Unit | GUI initialized | 1. Start app (default) | Light theme applied | ☐ |
| TC-003 | Styles | Dark Mode Toggle | Unit | App running | 1. Click "Dark Mode" checkbox | UI switches to dark theme | ☐ |
| TC-004 | Layout | Header Components | Unit | App running | 1. Check header elements | All inputs visible, buttons clickable | ☐ |
| TC-005 | Layout | Left Panel Loads | Unit | App running | 1. Check left panel | Sequence selector, treeview, progress bar visible | ☐ |
| TC-006 | Layout | Right Panel Loads | Unit | App running | 1. Check right panel | History, Bluetooth, builders visible | ☐ |
| TC-007 | Layout | Full Screen Mode | Unit | App running on Pi | 1. Launch app on Pi display | App maximizes to fill screen | ☐ |

---

## 2️⃣ **Configuration & Data Loading Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-008 | Config | Load config.py | Unit | config.py exists | 1. Start app | Timeout, results dir, test file loaded | ☐ |
| TC-009 | Config | Invalid config | Unit | config.py has errors | 1. Start app | Graceful error handling, default values used | ☐ |
| TC-010 | JSON | Load test_definitions.json | Unit | JSON file exists | 1. Start app | Sequences populate dropdown | ☐ |
| TC-011 | JSON | Malformed JSON | Unit | JSON has syntax errors | 1. Start app | Error logged, app doesn't crash | ☐ |
| TC-012 | Runner | Load Definitions | Integration | JSON valid | 1. runner.load_definitions() | defs dict populated, sequences listed | ☐ |
| TC-013 | Combo | Sequence Dropdown | Unit | JSON loaded | 1. Check dropdown | All sequences visible, selectable | ☐ |

---

## 3️⃣ **User Input Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-014 | Input | Enter Tester Name | Unit | App running | 1. Click tester field 2. Type name | Text entered, no validation errors | ☐ |
| TC-015 | Input | Enter Board ID | Unit | App running | 1. Click board field 2. Type ID | Text entered, no validation errors | ☐ |
| TC-016 | Input | Select Sequence | Unit | Dropdown loaded | 1. Click dropdown 2. Select sequence | Sequence selected, updated in UI | ☐ |
| TC-017 | Input | Checkbox - Continue on Fail | Unit | App running | 1. Toggle checkbox | State changes, reflected in UI | ☐ |
| TC-018 | Input | Empty Tester Name | Edge Case | App running | 1. Leave tester blank 2. Start test | Test runs with "Unknown" default | ☐ |
| TC-019 | Input | Long Board ID | Edge Case | App running | 1. Enter 100 char ID 2. Run test | Field accepts without truncation | ☐ |

---

## 4️⃣ **Test Execution Flow Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-020 | Runner | Single Test Execution | Integration | JSON loaded, test valid | 1. Select "Power Check" 2. Click Start | Test runs, result displays | ☐ |
| TC-021 | Runner | Full Sequence | Integration | All tests valid | 1. Select "Full Functional Suite" 2. Click Start | All 3 tests run in order | ☐ |
| TC-022 | Runner | Sequence Progress | Unit | Test running | 1. Watch execution | Progress bar fills, treeview updates | ☐ |
| TC-023 | Execution | Import Test Module | Unit | gpio_test/*.py exists | 1. Execute power_check test | Module imported successfully | ☐ |
| TC-024 | Execution | Missing Test Module | Error Handling | Test module doesn't exist | 1. Edit JSON to invalid test 2. Run | Error logged, test marked FAILED | ☐ |
| TC-025 | Execution | Execute Test with Mock GPIO | Unit | RPi.GPIO unavailable | 1. Run test without hardware | Mock GPIO returns fake data | ☐ |
| TC-026 | Execution | Execute Test with Real GPIO | Unit | RPi.GPIO available, hardware connected | 1. Run test on real Pi | Real sensor readings captured | ☐ |

---

## 5️⃣ **Hardware Abstraction Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-027 | GPIO | Mock GPIO Fallback | Unit | RPi.GPIO not installed | 1. Start test | mock_gpio.py used, no errors | ☐ |
| TC-028 | GPIO | Real GPIO Usage | Unit | RPi.GPIO installed, pins configured | 1. Start test | Real GPIO called, values read | ☐ |
| TC-029 | Power | Voltage Reading | Unit | ADC connected | 1. Run Power Check | Voltage value between 0-20V | ☐ |
| TC-030 | Power | Current Reading | Unit | Current sensor connected | 1. Run Power Check | Current value between 0-5A | ☐ |
| TC-031 | Sensor | ADC Ch0 Reading | Unit | ADC channel 0 connected | 1. Run Sensor Read | Value between 0-3.3V | ☐ |
| TC-032 | Sensor | ADC Ch1 Reading | Unit | ADC channel 1 connected | 1. Run Sensor Read | Value between 0-3.3V | ☐ |
| TC-033 | Button | Button Press Detection | Unit | Button connected to GPIO | 1. Run Button Press | Button state detected correctly | ☐ |

---

## 6️⃣ **Condition Evaluation Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-034 | Eval | Greater Than Condition | Unit | Test has `>= 11.5` condition | 1. Reading = 12V | Result = PASS | ☐ |
| TC-035 | Eval | Greater Than Fails | Unit | Test has `>= 11.5` condition | 1. Reading = 11.0V | Result = FAIL | ☐ |
| TC-036 | Eval | Range Condition Pass | Unit | Test has `0.5-1.5` range | 1. Reading = 1.0V | Result = PASS | ☐ |
| TC-037 | Eval | Range Condition Fail | Unit | Test has `0.5-1.5` range | 1. Reading = 2.0V | Result = FAIL | ☐ |
| TC-038 | Eval | Equal Condition Pass | Unit | Test has `== PRESSED` | 1. Reading = "Pressed" | Result = PASS | ☐ |
| TC-039 | Eval | Equal Condition Fail | Unit | Test has `== PRESSED` | 1. Reading = "Released" | Result = FAIL | ☐ |
| TC-040 | Eval | Multiple Subtests | Unit | Test has 3 subtests | 1. Run test | All subtests evaluated independently | ☐ |

---

## 7️⃣ **Result Display Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-041 | UI | Treeview Populated | Unit | Test executed | 1. Check treeview | Test name, status, duration, result visible | ☐ |
| TC-042 | UI | Color Coding - Pass | Unit | Test passed | 1. Check row color | Green background/border | ☐ |
| TC-043 | UI | Color Coding - Fail | Unit | Test failed | 1. Check row color | Red background/border | ☐ |
| TC-044 | UI | Expandable Rows | Unit | Treeview populated | 1. Double-click row | Subtests expand/collapse | ☐ |
| TC-045 | UI | Progress Bar Update | Unit | Test running | 1. Watch progress bar | Fills smoothly as test progresses | ☐ |
| TC-046 | UI | Status Label | Unit | Test executing | 1. Check status bar | Shows "Running...", then "Complete" | ☐ |

---

## 8️⃣ **Continue on Fail Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-047 | Runner | Stop on First Fail | Integration | "Continue on Fail" unchecked | 1. Run sequence with failing test 2. Check execution | Sequence stops at first failure | ☐ |
| TC-048 | Runner | Continue on Fail | Integration | "Continue on Fail" checked | 1. Run sequence with failing test | Sequence continues to next test | ☐ |
| TC-049 | Runner | Run Remaining Tests | Integration | Sequence failed, "Run Remaining" button visible | 1. Click "Run Remaining Tests" | Remaining tests execute | ☐ |

---

## 9️⃣ **Results Persistence Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-050 | Logger | Save Result JSON | Integration | Test executed | 1. Check results/ directory | JSON file created with timestamp | ☐ |
| TC-051 | Logger | Valid JSON Format | Unit | Result saved | 1. Parse JSON file | Valid JSON, matches schema | ☐ |
| TC-052 | Logger | Metadata Included | Unit | Result saved | 1. Open JSON file | Contains tester name, board ID, timestamp | ☐ |
| TC-053 | Logger | Results Directory | Unit | results/ doesn't exist | 1. Run test | Directory auto-created | ☐ |
| TC-054 | Logger | Invalid Path | Error | Results dir not writable | 1. Run test | Error logged, graceful failure | ☐ |

---

## 🔟 **History Management Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-055 | History | Load History List | Unit | results/ has JSON files | 1. Start app | History list populated | ☐ |
| TC-056 | History | Select History Item | Unit | History list populated | 1. Click history item | Details load in treeview | ☐ |
| TC-057 | History | Display JSON | Unit | History item selected | 1. Check JSON panel | Raw JSON displayed | ☐ |
| TC-058 | History | Max Items Limit | Unit | results/ has >100 files | 1. Check history list | Only 100 most recent shown | ☐ |
| TC-059 | History | Sorted by Date | Unit | Multiple history items | 1. Check list order | Most recent first | ☐ |
| TC-060 | History | Empty History | Edge Case | No results saved yet | 1. Check history panel | Shows "No history" message | ☐ |

---

## 1️⃣1️⃣ **Bluetooth Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-061 | BT | Scan for Devices | Integration | Bluetooth available, devices present | 1. Click "Start Scan" | Devices listed with RSSI | ☐ |
| TC-062 | BT | No Devices Found | Edge Case | No BLE devices nearby | 1. Click "Start Scan" | Shows "No devices found" | ☐ |
| TC-063 | BT | RSSI Signal Strength | Unit | Device found | 1. Check RSSI display | Shows dBm value and signal bars | ☐ |
| TC-064 | BT | Target Device Filtering | Unit | Device name matches prefix | 1. Scan and check list | Target devices marked [TARGET] | ☐ |
| TC-065 | BT | Connect Device | Integration | Device selected | 1. Click "Connect Selected" | Connection attempted, status shown | ☐ |
| TC-066 | BT | Scan Timeout | Unit | Scan in progress | 1. Wait >10s | Scan completes with results | ☐ |

---

## 1️⃣2️⃣ **Error Handling Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-067 | Error | Module Import Error | Error Handling | Invalid module path | 1. Run test with bad path | Error logged, test marked FAILED | ☐ |
| TC-068 | Error | Test Timeout | Error Handling | Test exceeds timeout | 1. Wait for timeout | Test marked TIMEOUT/FAILED | ☐ |
| TC-069 | Error | Condition Parse Error | Error Handling | Invalid condition syntax | 1. Run test with bad condition | Error logged, test marked FAILED | ☐ |
| TC-070 | Error | Hardware Connection Error | Error Handling | GPIO pin unavailable | 1. Run test on disconnected hardware | Error caught, graceful failure | ☐ |
| TC-071 | Error | JSON Corruption | Error Handling | History file corrupted | 1. Click corrupted result | Error shown, app doesn't crash | ☐ |
| TC-072 | Error | Disk Full | Error Handling | Storage full | 1. Run test | Error logged, operation fails gracefully | ☐ |

---

## 1️⃣3️⃣ **Integration Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-073 | Integration | Full Workflow | E2E | All systems ready | 1. Enter details 2. Select sequence 3. Run 4. View history | Complete flow works end-to-end | ☐ |
| TC-074 | Integration | Multiple Sequences | E2E | App running | 1. Run Full Suite 2. Run Power-Only 3. Check history | Both results saved, both visible in history | ☐ |
| TC-075 | Integration | Settings Persistence | E2E | Dark mode changed | 1. Toggle dark mode 2. Run test 3. Check UI | Dark mode maintained during execution | ☐ |
| TC-076 | Integration | Results Flow | E2E | Test completed | 1. Execute test 2. Check UI 3. Check file | Result in UI, file, and history | ☐ |

---

## 1️⃣4️⃣ **Performance Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-077 | Performance | Startup Time | Perf | App ready to launch | 1. Measure startup to window visible | < 5 seconds | ☐ |
| TC-078 | Performance | Sequence Execution | Perf | 3-test sequence | 1. Measure total time | Completes in < 3 minutes | ☐ |
| TC-079 | Performance | History Load | Perf | 100 result files | 1. Measure history load time | < 2 seconds | ☐ |
| TC-080 | Performance | Bluetooth Scan | Perf | Multiple BT devices | 1. Measure scan time | < 10 seconds | ☐ |
| TC-081 | Performance | Memory Usage | Perf | App running | 1. Monitor memory during execution | < 500MB | ☐ |

---

## 1️⃣5️⃣ **Cross-Platform Tests**

| ID | Component | Test Scenario | Test Type | Prerequisites | Steps | Expected Result | Status |
|----|-----------|---------------|-----------|---------------|-------|-----------------|--------|
| TC-082 | Platform | Windows Execution | Integration | Windows 10/11 + Python | 1. Run on Windows | App launches, all features work | ☐ |
| TC-083 | Platform | Linux Execution | Integration | Linux + Python | 1. Run on Linux | App launches, all features work | ☐ |
| TC-084 | Platform | Pi OS Execution | Integration | Raspberry Pi OS + Python | 1. Run on Pi | Full-screen mode works | ☐ |
| TC-085 | Platform | macOS Execution | Integration | macOS + Python | 1. Run on macOS | App launches, all features work | ☐ |
| TC-086 | Platform | Different Screen Sizes | UI | Multiple resolutions | 1. Run at 1920x1080, 1280x720, 4K | UI scales appropriately | ☐ |

---

## Summary Statistics

| Category | Test Count | Status |
|----------|-----------|--------|
| **Initialization** | 7 | ☐ |
| **Configuration** | 6 | ☐ |
| **User Input** | 6 | ☐ |
| **Test Execution** | 6 | ☐ |
| **Hardware Abstraction** | 7 | ☐ |
| **Condition Evaluation** | 7 | ☐ |
| **Result Display** | 6 | ☐ |
| **Continue on Fail** | 3 | ☐ |
| **Results Persistence** | 5 | ☐ |
| **History Management** | 6 | ☐ |
| **Bluetooth** | 6 | ☐ |
| **Error Handling** | 6 | ☐ |
| **Integration** | 4 | ☐ |
| **Performance** | 5 | ☐ |
| **Cross-Platform** | 5 | ☐ |
| **TOTAL** | **86 Test Cases** | **☐** |

---

## 🎯 How to Use This Matrix

1. **For Development**: Run tests as you develop each component
2. **For QA**: Use to verify all functionality before release
3. **For Documentation**: Reference which components are tested
4. **For Coverage**: Identify gaps in testing
5. **For Regression**: Re-run after changes

## ✅ Test Execution Guidelines

- **Unit Tests**: Run during development
- **Integration Tests**: Run after features complete
- **E2E Tests**: Run before release
- **Performance Tests**: Run on target hardware (Pi)
- **Cross-Platform**: Run on all supported OSes

## 📝 Notes

- Status column (☐) can be marked with:
  - ☐ = Not Started
  - ◐ = In Progress
  - ☑ = Passed
  - ✘ = Failed
  - ⊘ = Not Applicable

- Update this matrix as new features are added
- Document any failed tests with screenshots/logs
- Use for Senior Design project documentation
