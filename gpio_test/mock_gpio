import random
import time


class MockSerial:
    """
    A deterministic Arduino-style mock serial interface.
    """

    def __init__(self):
        self._last_command = None
        self._response_ready = False
        self._response_value = None

    def write(self, command: str):
        """
        Accept a command and prepare a mock response.
        """
        self._last_command = command.strip().upper()
        self._response_ready = False

        # Simulate Arduino processing delay
        time.sleep(0.02)

        # Map commands to mock values
        if self._last_command == "VOLTAGE":
            self._response_value = round(random.uniform(11.8, 12.2), 3)

        elif self._last_command == "CURRENT":
            self._response_value = round(random.uniform(0.01, 0.05), 3)

        elif self._last_command == "ADC0":
            self._response_value = round(random.uniform(1.10, 1.30), 3)

        elif self._last_command == "ADC1":
            self._response_value = round(random.uniform(1.00, 1.20), 3)

        elif self._last_command == "BTN1":
            self._response_value = random.choice(["Pressed", "Released"])

        elif self._last_command == "BTN2":
            self._response_value = random.choice(["Pressed", "Released"])

        else:
            self._response_value = None

        self._response_ready = True

    def read(self):
        """
        Return the prepared response if ready.
        """
        if self._response_ready:
            self._response_ready = False
            return self._response_value
        return None
