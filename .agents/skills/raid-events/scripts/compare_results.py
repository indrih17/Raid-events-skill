#!/usr/bin/env python3
"""Compare explicit normalised SimC observations; never infer causal mechanics."""
import argparse
import json
import math
from pathlib import Path


def number(value, field):
    if isinstance(value, dict):
        if "mean" not in value:
            raise ValueError(f"{field}: sample object has no mean")
        value = value["mean"]
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{field}: expected a numeric mean")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{field}: expected finite nonnegative value")
    return float(value)


def validate_case(case):
    if not isinstance(case, dict):
        raise ValueError("case must be an object")
    for field in ("label", "action", "owner", "damage_scope"):
        if not isinstance(case.get(field), str) or not case[field].strip():
            raise ValueError(f"case requires nonempty {field}")
    out = dict(case)
    for field in ("num_executes", "num_direct_results", "damage"):
        if field not in case:
            raise ValueError(f"missing {field}; do not assume zero")
        out[field] = number(case[field], field)
    if out["num_executes"] == 0 and out["num_direct_results"] > 0:
        out["warning"] = "Results with zero executions: inspect tick/child/stat semantics."
    out["direct_results_per_execution"] = (
        out["num_direct_results"] / out["num_executes"]
        if out["num_executes"] else None
    )
    return out


def compare(document):
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("expected normalised schema_version=1")
    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    result = [validate_case(case) for case in cases]
    if len({c["label"] for c in result}) != len(result):
        raise ValueError("duplicate case label")
    baseline = result[0]
    for case in result[1:]:
        for field in ("action", "owner", "damage_scope"):
            if case[field] != baseline[field]:
                raise ValueError(f"incompatible {field}: normalise scopes before comparison")
    deltas = []
    for case in result[1:]:
        delta = {"label": case["label"], "baseline": baseline["label"]}
        for field in ("num_executes", "num_direct_results", "damage"):
            base = baseline[field]
            delta[field] = {
                "absolute": case[field] - base,
                "percent": 100 * (case[field] / base - 1) if base else None,
            }
        deltas.append(delta)
    return {"schema_version": 1, "cases": result, "deltas": deltas,
            "interpretation": "Ratios of means; no causal or significance inference."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="Print machine-readable comparison")
    args = parser.parse_args()
    try:
        documents = [json.loads(p.read_text(encoding="utf-8-sig")) for p in args.inputs]
        for doc in documents:
            if not isinstance(doc, dict) or doc.get("schema_version") != 1:
                raise ValueError("expected schema_version=1 in each input")
            if not isinstance(doc.get("cases"), list):
                raise ValueError("cases must be a list in each input")
        result = compare({"schema_version": 1,
                          "cases": [case for doc in documents for case in doc["cases"]]})
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        else:
            print("label | executes | direct results | results/execution | reported damage")
            for c in result["cases"]:
                ratio = c["direct_results_per_execution"]
                text = "undefined" if ratio is None else f"{ratio:.9f}"
                print(f'{c["label"]} | {c["num_executes"]:.3f} | '
                      f'{c["num_direct_results"]:.3f} | {text} | {c["damage"]:.3f}')
            for delta in result["deltas"]:
                print(f'\n{delta["label"]} vs {delta["baseline"]}:')
                for field in ("num_executes", "num_direct_results", "damage"):
                    d = delta[field]
                    pct = "undefined" if d["percent"] is None else f'{d["percent"]:+.6f}%'
                    print(f'  {field}: {d["absolute"]:+.3f} ({pct})')
            print("\n" + result["interpretation"])
    except (OSError, ValueError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
