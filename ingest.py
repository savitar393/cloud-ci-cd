import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen

API_URL = "https://api.data.gov.sg/v1/transport/carpark-availability"
SGT = timezone(timedelta(hours=8))


def save_snapshot(payload, root=Path("data")):
    items = payload.get("items")
    if not items:
        raise ValueError("API did not return any snapshots")

    snapshot = items[0]
    if not snapshot.get("carpark_data"):
        raise ValueError("Snapshot contains no carpark data")

    stamp = datetime.fromisoformat(snapshot["timestamp"])
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=SGT)
    stamp = stamp.astimezone(SGT)

    path = root / (
        f"carpark_availability/year={stamp:%Y}/month={stamp:%m}/"
        f"day={stamp:%d}/{stamp:%Y%m%dT%H%M%S}_SGT.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    with urlopen(API_URL, timeout=30) as response:
        payload = json.load(response)
    print(save_snapshot(payload).as_posix())