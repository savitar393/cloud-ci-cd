import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ingest import save_snapshot


class IngestTests(unittest.TestCase):
    def test_saves_snapshot_using_singapore_date(self):
        payload = {"items": [{
            "timestamp": "2026-11-24T18:30:00+00:00",
            "carpark_data": [{"carpark_number": "HE12"}],
        }]}
        with TemporaryDirectory() as folder:
            root = Path(folder)
            path = save_snapshot(payload, root)
            self.assertEqual(
                path.relative_to(root).as_posix(),
                "carpark_availability/year=2026/month=11/day=25/20261125T023000_SGT.json",
            )
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), payload)

    def test_rejects_empty_response(self):
        with self.assertRaisesRegex(ValueError, "did not return any snapshots"):
            save_snapshot({"items": []})