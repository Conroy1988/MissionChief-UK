#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

HTML_ROUTES = (
    "",
    "tools/mission-lookup/",
    "tools/resource-comparison/",
    "tools/fleet-planner/",
    "tools/query-catalogue/",
    "reference/generated-faq/",
    "api/",
    "releases/v1.0.0/",
)

API_FILES = (
    "manifest.json",
    "missions.json",
    "vehicles.json",
    "infrastructure.json",
    "training.json",
    "search-index.json",
    "faq.json",
    "openapi.json",
)


class SmokeFailure(RuntimeError):
    pass


def fetch(url: str, attempts: int, delay: float) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = Request(url, headers={"User-Agent": "MissionChief-UK-release-smoke/1.0"})
            with urlopen(request, timeout=30) as response:
                body = response.read()
                content_type = response.headers.get_content_type()
                if response.status != 200:
                    raise SmokeFailure(f"{url} returned HTTP {response.status}")
                if not body:
                    raise SmokeFailure(f"{url} returned an empty body")
                return body, content_type
        except (HTTPError, URLError, TimeoutError, SmokeFailure) as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(delay)
    raise SmokeFailure(f"Unable to fetch {url} after {attempts} attempts: {last_error}")


def parse_json(body: bytes, url: str) -> Any:
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SmokeFailure(f"Invalid JSON returned by {url}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test the deployed MissionChief UK Pages site")
    parser.add_argument("base_url", help="Deployed Pages base URL")
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=float, default=5.0)
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/") + "/"
    api_root = urljoin(base_url, "assets/data/v1/")

    try:
        for route in HTML_ROUTES:
            url = urljoin(base_url, route)
            body, content_type = fetch(url, args.attempts, args.delay)
            require("html" in content_type, f"Expected HTML content type from {url}, received {content_type}")
            text = body.decode("utf-8", errors="replace")
            require("MissionChief UK" in text, f"Expected MissionChief UK page marker was absent from {url}")

        script_url = urljoin(base_url, "javascripts/intelligence-tools.js")
        script, _ = fetch(script_url, args.attempts, args.delay)
        require(b"initMissionLookup" in script, "Deployed intelligence-tools.js is incomplete")

        payloads: dict[str, Any] = {}
        for filename in API_FILES:
            url = urljoin(api_root, filename)
            body, content_type = fetch(url, args.attempts, args.delay)
            require(content_type in {"application/json", "text/plain", "application/octet-stream"},
                    f"Unexpected content type for {url}: {content_type}")
            payloads[filename] = parse_json(body, url)

        manifest = payloads["manifest.json"]
        require(manifest.get("api_version") == "v1", "Deployed manifest api_version is not v1")
        require(manifest.get("data_version") == "1.0.0", "Deployed data version is not 1.0.0")
        require(manifest.get("stage") == 34, "Deployed manifest is not Stage 34")
        require(manifest.get("status") == "production", "Deployed manifest status is not production")

        collections = manifest.get("collections")
        require(isinstance(collections, dict), "Deployed manifest collections are invalid")
        total = 0
        for name in ("missions", "vehicles", "infrastructure", "training"):
            payload = payloads[f"{name}.json"]
            records = payload.get("records")
            require(isinstance(records, list), f"Deployed {name} records are invalid")
            require(payload.get("data_version") == manifest.get("data_version"), f"Deployed {name} version mismatch")
            require(payload.get("count") == len(records), f"Deployed {name} count does not match records")
            require(collections.get(name, {}).get("count") == len(records), f"Manifest count mismatch for {name}")
            total += len(records)

        search_index = payloads["search-index.json"]
        require(search_index.get("count") == total, "Deployed search-index count does not match collection totals")
        require(len(search_index.get("records", [])) == total, "Deployed search-index records are incomplete")

        faq = payloads["faq.json"]
        require(faq.get("data_version") == manifest.get("data_version"), "Deployed FAQ version mismatch")
        require(faq.get("count") == len(faq.get("entries", [])), "Deployed FAQ count mismatch")

        openapi = payloads["openapi.json"]
        require(openapi.get("openapi") == "3.1.0", "Deployed OpenAPI contract is not version 3.1.0")
        require(openapi.get("info", {}).get("version") == manifest.get("data_version"), "Deployed OpenAPI version mismatch")
    except SmokeFailure as exc:
        print(f"Pages smoke test failed: {exc}")
        return 1

    print(f"Pages smoke test passed for {base_url} ({total} indexed records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
