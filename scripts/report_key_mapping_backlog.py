#!/usr/bin/env python3

from __future__ import annotations

import report_key_mapping_backlog_base as _base
from report_key_mapping_backlog_base import *  # noqa: F401,F403

_base.SAFE_ADDITIONAL_KEYS.add("need_traffic_car_only_if_present")

build_report = _base.build_report
main = _base.main

if __name__ == "__main__":
    raise SystemExit(main())
