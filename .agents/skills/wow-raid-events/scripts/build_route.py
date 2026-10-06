#!/usr/bin/env python3
"""Generate a raid-events overlay from a reconstructed GUID target ledger."""
import argparse
import json
import re
from pathlib import Path

from compare_results import number

NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def fmt(value):
    return f"{value:.12g}"


def validate(document):
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("expected timeline schema_version=1")
    duration = number(document.get("duration"), "duration")
    if duration <= 0:
        raise ValueError("duration must be positive")
    targets = document.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ValueError("targets must be nonempty")
    seen_guid, seen_names = set(), set()
    clean = []
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError("target must be an object")
        guid = target.get("guid")
        if not isinstance(guid, str) or not guid.strip():
            raise ValueError("each target needs spawn GUID")
        if guid in seen_guid:
            raise ValueError(f"duplicate GUID {guid}: resolve chain pulls/windows before generation")
        seen_guid.add(guid)
        pull = target.get("pull")
        if isinstance(pull, bool) or not isinstance(pull, int) or pull < 1:
            raise ValueError("pull must be a positive integer")
        name = target.get("name")
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise ValueError("target name must use safe ASCII letters/digits/underscore")
        final_name = f"{name}_P{pull:02d}"
        if final_name in seen_names:
            raise ValueError(f"name collision {final_name}; use unique spawn names")
        seen_names.add(final_name)
        start, end = number(target.get("start"), "start"), number(target.get("end"), "end")
        if end <= start or end > duration:
            raise ValueError(f"{guid}: require 0 <= start < end <= duration")
        if target.get("kind") not in ("trash", "boss"):
            raise ValueError(f"{guid}: kind must be trash or boss")
        if target.get("origin") not in ("initial", "spawned"):
            raise ValueError(f"{guid}: origin must be initial or spawned")
        if target.get("confidence") not in ("confirmed", "estimated"):
            raise ValueError(f"{guid}: confidence must be confirmed or estimated")
        evidence = target.get("evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError(f"{guid}: evidence required")
        if "\n" in evidence or "\r" in evidence:
            raise ValueError("evidence must be a single-line note")
        npc_id = target.get("npc_id")
        if npc_id is not None and (isinstance(npc_id, bool) or not isinstance(npc_id, int) or npc_id <= 0):
            raise ValueError("npc_id must be a positive integer when provided")
        clean.append({**target, "start": start, "end": end, "simc_name": final_name})
    bl = document.get("bloodlust", [])
    if not isinstance(bl, list):
        raise ValueError("bloodlust must be a list of timestamps")
    bl = [number(t, "bloodlust timestamp") for t in bl]
    if bl != sorted(set(bl)) or any(t >= duration for t in bl):
        raise ValueError("bloodlust timestamps must be unique, increasing and before route end")
    return duration, clean, bl


def generate(document, exact=False):
    duration, targets, bl = validate(document)
    cooldown = max(5160.0, duration + 1)
    dummy_duration = duration + 1
    lines = [
        "# Generated teaching encounter overlay; a player profile is required.",
        "# SimC parsing and runtime validation must be performed separately.",
        "# Mode: " + ("fixed lifetime bounds" if exact else "route approximation; duration_stddev=1"),
        "fight_style=Patchwerk", "fixed_time=1", f"max_time={fmt(duration)}",
        "vary_combat_length=0", "strict_parsing=1",
        "active_enemies=1", "ignore_invulnerable_targets=1", "override.bloodlust=0",
        "# Baseline anchor unavailable throughout the route; one timestamp start.",
        f"raid_events=/invulnerable,timestamps=0,cooldown={fmt(cooldown)},"
        f"duration={fmt(dummy_duration)},duration_min={fmt(dummy_duration)},"
        f"duration_max={fmt(dummy_duration)},retarget=1",
    ]
    last_pull = None
    for target in sorted(targets, key=lambda t: (t["pull"], t["start"], t["simc_name"])):
        if target["pull"] != last_pull:
            last_pull = target["pull"]
            lines += ["# ============================================================",
                      f"# PULL {last_pull}",
                      "# ============================================================"]
        lines.append(f'# {target["confidence"]}; {target["origin"]}; {target["evidence"]}')
        lifetime = target["end"] - target["start"]
        event = (f'raid_events+=/adds,name={target["simc_name"]},'
                 f'timestamps={fmt(target["start"])},count=1,cooldown={fmt(cooldown)},'
                 f'duration={fmt(lifetime)}')
        if exact:
            event += f",duration_min={fmt(lifetime)},duration_max={fmt(lifetime)}"
        else:
            event += ",duration_stddev=1"
        if target["kind"] == "boss":
            event += ",type=add_boss"
        lines.append(event)
    if bl:
        lines += ["# Bloodlust uses absolute timestamps rather than pull numbers.",
                  "raid_events+=/buff,buff_name=bloodlust,duration=40,"
                  "duration_min=40,duration_max=40,timestamps=" + ":".join(map(fmt, bl))]
    lines.append("# This overlay does not configure priority targeting or geometry.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", type=Path)
    parser.add_argument("--exact", action="store_true", help="Use fixed duration bounds")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        text = generate(json.loads(args.timeline.read_text(encoding="utf-8-sig")), args.exact)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
