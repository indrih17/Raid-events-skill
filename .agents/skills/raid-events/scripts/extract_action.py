#!/usr/bin/env python3
"""Extract one explicitly selected action from a sim.players JSON report."""
import argparse
import hashlib
import json
from pathlib import Path

from compare_results import number, validate_case


def walk_stats(rows, location):
    if not isinstance(rows, list):
        raise ValueError(f"{location}: stats must be a list")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{location}: invalid stats entry")
        path = f"{location}[{index}]"
        yield row, path
        if "children" in row:
            yield from walk_stats(row["children"], path + ".children")


def extract(report, player, action, label, damage_field="actual_amount",
            pet=None, missing_zero=False):
    if damage_field not in ("actual_amount", "compound_amount"):
        raise ValueError("unsupported damage field")
    if not isinstance(report, dict):
        raise ValueError("report must be an object")
    sim = report.get("sim")
    if not isinstance(sim, dict) or not isinstance(sim.get("players"), list):
        raise ValueError("unsupported report: expected sim.players")
    matches = [p for p in sim["players"] if isinstance(p, dict) and p.get("name") == player]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one player named {player!r}; found {len(matches)}")
    actor = matches[0]
    if pet is None:
        rows = actor.get("stats")
        location = f"sim.players[{player}].stats"
        owner = player
    else:
        pets = actor.get("stats_pets")
        if not isinstance(pets, dict) or pet not in pets:
            raise ValueError(f"pet stats not found: {pet!r}")
        rows = pets[pet]
        location = f"sim.players[{player}].stats_pets[{pet}]"
        owner = f"{player}/pet:{pet}"
    candidates = [(row, path) for row, path in walk_stats(rows, location)
                  if row.get("name") == action]
    if len(candidates) != 1:
        raise ValueError(f"expected exactly one action {action!r}; found {len(candidates)}")
    row, path = candidates[0]
    omitted = []
    def metric(key):
        if key not in row:
            if missing_zero and key in ("num_direct_results", "actual_amount"):
                omitted.append(key)
                return 0.0
            raise ValueError(f"{key} missing at {path}; inspect report or explicitly use --missing-zero")
        return number(row[key], key)
    case = {"label": label, "owner": owner, "action": action,
            "num_executes": metric("num_executes"),
            "num_direct_results": metric("num_direct_results"),
            "damage": metric(damage_field), "damage_scope": damage_field,
            "source_json_path": path, "spell_id": row.get("id"),
            "omitted_fields_assumed_zero": omitted}
    validate_case(case)
    return {"schema_version": 1, "cases": [case]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--player", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--pet", help="Exact stats_pets owner name; pets excluded by default")
    parser.add_argument("--damage-field", choices=("actual_amount", "compound_amount"),
                        default="actual_amount")
    parser.add_argument("--missing-zero", action="store_true",
                        help="Explicitly treat omitted zero-able result/actual fields as zero")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        raw = args.report.read_bytes()
        result = extract(json.loads(raw.decode("utf-8-sig")), args.player, args.action,
                         args.label, args.damage_field, args.pet, args.missing_zero)
        result["source"] = {"file": str(args.report),
                            "sha256": hashlib.sha256(raw).hexdigest(),
                            "status": "extracted, not independently reproduced"}
        text = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
