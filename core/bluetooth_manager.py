import asyncio
from typing import List, Dict, Optional

from bleak import BleakScanner, BleakClient


class BluetoothManager:
    """
    Handles BLE scanning and simple connection checks.
    """

    def __init__(self, target_name_prefix: Optional[str] = None):
        # If set, we treat devices whose name starts with this as "target" devices.
        self.target_name_prefix = target_name_prefix
        self.last_scan_results: List[Dict] = []

    async def scan_devices(self, timeout: int = 1) -> List[Dict]:
        """
        Scan for BLE devices for `timeout` seconds.
        Returns a list of dicts: {name, address, rssi, is_target}.
        """
        devices = await BleakScanner.discover(timeout=timeout)
        results = []

        for d in devices:
            name = d.name or "Unknown"
            is_target = False
            if self.target_name_prefix and name:
                is_target = name.startswith(self.target_name_prefix)

            results.append(
                {
                    "name": name,
                    "address": d.address,
                    "rssi": d.rssi,
                    "is_target": is_target,
                }
            )

        self.last_scan_results = results
        return results

    async def connect_and_check(self, address: str, timeout: int = 10) -> bool:
        """
        Try to connect to a BLE device by address.
        Returns True if connection succeeds, False otherwise.
        """
        try:
            async with BleakClient(address, timeout=timeout) as client:
                return client.is_connected
        except Exception:
            return False
