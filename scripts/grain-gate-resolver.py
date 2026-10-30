#!/usr/bin/env python3
"""Evaluate one admitted PC grain-gate opening request from asset-free JSON.

The input is either a path or ``-`` for stdin.  This reporting surface reads
only that JSON, writes only deterministic JSON to stdout, and never opens game
assets or a target process.

Tunnels schema::

    {
      "family": "tunnels", "internal_level": 3,
      "flik_x": 501696, "flik_z": 494016, "grain_count": 10,
      "radius": 100,
      "records": [
        {"type_value": 4295, "unknown_04": 26, "requirement": 20,
         "center_x": 193754, "center_z": 131692}
      ]
    }

``records`` must contain all nine ordered rows.  City schema::

    {
      "family": "city_entrance", "internal_level": 4,
      "flik_x": -87622, "flik_z": -182181, "grain_count": 10,
      "gate": {"index": 0, "state": -1, "requirement": 10,
               "center_x": -71129, "center_z": -184314, "radius": 80,
               "delta_a": -32, "delta_b": 32, "slot_a": 2, "slot_b": 3}
    }

Evidence and boundary: :mod:`ablpc.grain_gate_resolver`, EXP-20260816-166,
EXP-20260816-168, and EXP-20260816-169.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))

from ablpc.grain_gate_resolver import (  # noqa: E402
    BUGS_EXE_SHA256,
    CityGate,
    CityRequest,
    GrainGateResolverError,
    TunnelsRecord,
    TunnelsRequest,
    resolve_city,
    resolve_tunnels,
)


def _object(value: Any, *, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) for key in value
    ):
        raise GrainGateResolverError(f"{label} must be a JSON object")
    return value


def _exact_keys(
    value: dict[str, Any],
    *,
    required: set[str],
    optional: set[str] = frozenset(),
    label: str,
) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing:
        raise GrainGateResolverError(
            f"{label} is missing keys: {', '.join(sorted(missing))}"
        )
    if extra:
        raise GrainGateResolverError(
            f"{label} has unknown keys: {', '.join(sorted(extra))}"
        )


def _tunnels_request(payload: dict[str, Any]) -> TunnelsRequest:
    required = {"family", "internal_level", "flik_x", "flik_z", "grain_count", "records"}
    _exact_keys(
        payload,
        required=required,
        optional={"radius"},
        label="Tunnels request",
    )
    raw_records = payload["records"]
    if not isinstance(raw_records, list):
        raise GrainGateResolverError("Tunnels records must be a JSON array")
    records = []
    record_keys = {
        "type_value",
        "unknown_04",
        "requirement",
        "center_x",
        "center_z",
    }
    for index, raw_record in enumerate(raw_records):
        record = _object(raw_record, label=f"Tunnels record {index}")
        _exact_keys(
            record,
            required=record_keys,
            label=f"Tunnels record {index}",
        )
        records.append(TunnelsRecord(**record))
    kwargs = {
        "internal_level": payload["internal_level"],
        "flik_x": payload["flik_x"],
        "flik_z": payload["flik_z"],
        "grain_count": payload["grain_count"],
        "records": tuple(records),
    }
    if "radius" in payload:
        kwargs["radius"] = payload["radius"]
    return TunnelsRequest(**kwargs)


def _city_request(payload: dict[str, Any]) -> CityRequest:
    _exact_keys(
        payload,
        required={
            "family",
            "internal_level",
            "flik_x",
            "flik_z",
            "grain_count",
            "gate",
        },
        label="City request",
    )
    gate = _object(payload["gate"], label="City gate")
    _exact_keys(
        gate,
        required={
            "index",
            "state",
            "requirement",
            "center_x",
            "center_z",
            "radius",
            "delta_a",
            "delta_b",
            "slot_a",
            "slot_b",
        },
        label="City gate",
    )
    return CityRequest(
        internal_level=payload["internal_level"],
        flik_x=payload["flik_x"],
        flik_z=payload["flik_z"],
        grain_count=payload["grain_count"],
        gate=CityGate(**gate),
    )


def build_report(payload: dict[str, Any]) -> dict[str, Any]:
    family = payload.get("family")
    if family == "tunnels":
        result = resolve_tunnels(_tunnels_request(payload))
    elif family == "city_entrance":
        result = resolve_city(_city_request(payload))
    else:
        raise GrainGateResolverError(
            "family must be 'tunnels' or 'city_entrance'"
        )
    return {
        "contract": {
            "binary_sha256": BUGS_EXE_SHA256,
            "scope": "twelve_confirmed_tunnels_city_mechanisms",
            "global_family_exclusivity_claimed": False,
            "address_0x00599C69_semantics": "Unknown",
            "executes_downstream_rules": False,
            "writes_files_or_target_state": False,
        },
        "result": asdict(result),
    }


def _read_payload(path: str) -> dict[str, Any]:
    if path == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(path).read_text(encoding="utf-8")
    try:
        value = json.loads(raw, object_pairs_hook=_unique_object)
    except json.JSONDecodeError as error:
        raise GrainGateResolverError(f"invalid JSON: {error}") from error
    return _object(value, label="request")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build one JSON object while refusing duplicate member names."""

    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GrainGateResolverError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pure offline PC Tunnels/City grain-gate opening resolver"
    )
    parser.add_argument("input", help="asset-free JSON request path, or - for stdin")
    args = parser.parse_args(argv)
    try:
        report = build_report(_read_payload(args.input))
    except (GrainGateResolverError, OSError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
