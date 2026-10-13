import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
TIMEOUT_SECONDS = 20
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "data" / "raw" / "api_snapshot.json"


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else API_URL
    print("requesting:", url)
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print("request failed:", error)
        sys.exit(1)

    retrieved_at = datetime.now(timezone.utc).isoformat()
    print("status:", response.status_code)
    print("content-type:", response.headers.get("Content-Type"))

    try:
        payload = response.json()
    except ValueError as error:
        print("response is not valid JSON:", error)
        sys.exit(1)

    print("top-level type:", type(payload).__name__)
    if isinstance(payload, list):
        print("number of records:", len(payload))
        sample = payload[0] if payload else None
    elif isinstance(payload, dict):
        print("number of top-level keys:", len(payload))
        print("top-level keys:", list(payload.keys()))
        sample = {key: payload[key] for key in list(payload)[:1]}
    else:
        sample = payload
    print("sample record:")
    print(json.dumps(sample, indent=2, ensure_ascii=False))

    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_bytes(response.content)
    print("snapshot saved to:", SNAPSHOT_PATH.relative_to(ROOT))
    print("retrieved_at_utc:", retrieved_at)


if __name__ == "__main__":
    main()