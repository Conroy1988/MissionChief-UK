#!/usr/bin/env python3

from __future__ import annotations

import report_canonical_candidates_base as _base
from report_canonical_candidates_base import *  # noqa: F401,F403

_base.SAFE_ADDITIONAL_KEYS.add("need_traffic_car_only_if_present")

report = _base.report
main = _base.main

if __name__ == "__main__":
    raise SystemExit(main())
