import time
from gpio_test.serial_mock import MockSerial


# Global singleton mock serial instance
_serial = MockSerial()


def read_value(command: str, timeout: float = 1.0):
    """
    Send a command to the mock Arduino and return a reading.
    """
    start = time.time()
    _serial.write(command)

    while True:
        if time.time() - start > timeout:
            return None  # timeout

        response = _serial.read()
        if response is not None:
            return response

        time.sleep(0.01)
