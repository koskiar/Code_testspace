import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    from gpio_test.mock_gpio import GPIO

def run(test_def: dict) -> dict:
    start = time.time()

    # Fake ADC readings
    adc0 = 1.23
    adc1 = 1.11

    subtests = []
    overall = "PASS"

    for sub in test_def["subtests"]:
        name = sub["name"]
        cond = sub["condition"]
        units = sub.get("units", "")

        if "Ch 0" in name:
            reading = adc0
        else:
            reading = adc1

        result = evaluate_condition(reading, cond)
        if result == "FAIL":
            overall = "FAIL"

        subtests.append({
            "name": name,
            "reading": reading,
            "units": units,
            "condition": cond,
            "result": result
        })

    end = time.time()

    return {
        "name": "Sensor Read",
        "time_started": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(start)),
        "time_ended": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(end)),
        "result": overall,
        "subtests": subtests
    }

def evaluate_condition(reading, cond: str) -> str:
    cond = cond.strip()
    try:
        if "-" in cond:
            low, high = cond.split("-")
            low = float(low)
            high = float(high)
            return "PASS" if low <= reading <= high else "FAIL"
        elif cond.startswith(">="):
            val = float(cond[2:].strip())
            return "PASS" if reading >= val else "FAIL"
        elif cond.startswith("<="):
            val = float(cond[2:].strip())
            return "PASS" if reading <= val else "FAIL"
        else:
            return "PASS"
    except Exception:
        return "FAIL"

