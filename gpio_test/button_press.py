import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    from gpio_test.mock_gpio import GPIO

def run(test_def: dict) -> dict:
    start = time.time()

    # Fake button states
    button1 = "Pressed"
    button2 = "Pressed"

    subtests = []
    overall = "PASS"

    for sub in test_def["subtests"]:
        name = sub["name"]
        cond = sub["condition"]
        units = sub.get("units", "")

        if "Button 1" in name:
            reading = button1
        else:
            reading = button2

        result = "PASS" if reading == cond else "FAIL"
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
        "name": "Button Press",
        "time_started": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(start)),
        "time_ended": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(end)),
        "result": overall,
        "subtests": subtests
    }
