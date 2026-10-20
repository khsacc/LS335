import json
import sys
import unittest
from pathlib import Path
from urllib.request import urlopen

# This test also runs when LS335 is cloned outside bl18c_controller.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lakeshore335_backend import DataPoint, LakeShore335Backend
from lakeshore335_readings_api import LakeShore335ReadingsServer


class CachedReadingsTests(unittest.TestCase):
    def test_http_reads_cached_temperatures_and_setpoint(self):
        backend = LakeShore335Backend(simulate=True)
        backend._connected = True
        backend.set_setpoint(220.0)
        with backend._buf_lock:
            backend._data.append(DataPoint(123.0, 210.5, 211.2, 220.0, 1))

        server = LakeShore335ReadingsServer(backend, port=0)
        server.start()
        try:
            url = f"http://127.0.0.1:{server._server.server_port}/api/v1/readings"
            with urlopen(url, timeout=2) as response:
                data = json.load(response)
            self.assertEqual(data, {
                "connected": True,
                "timestamp": 123.0,
                "temperature_a_k": 210.5,
                "temperature_b_k": 211.2,
                "target_setpoint_k": 220.0,
            })
        finally:
            server.stop()

        backend._connected = False
        self.assertIsNone(backend.get_cached_readings()["temperature_a_k"])
        self.assertIsNone(backend.get_cached_readings()["target_setpoint_k"])


if __name__ == "__main__":
    unittest.main()
