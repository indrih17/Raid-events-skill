#!/usr/bin/env python3
"""Check internal links, source preservation and bundled fixtures, not SimC mechanics."""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

from build_route import validate
from compare_results import compare

ORIGINAL_BLOB = "248e16dfa99740f6ac6a25f2a3f11491cf553df1"


def check_skill(path):
    """Validate this skill's deliberately simple two-scalar YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["missing or invalid skill frontmatter"]
    fields = {}
    for line in match.group(1).splitlines():
        if ": " not in line:
            return ["frontmatter must use simple name/description scalar fields"]
        key, value = line.split(": ", 1)
        if key in fields:
            return ["duplicate frontmatter field"]
        fields[key] = value
    if set(fields) != {"name", "description"}:
        return ["frontmatter requires exactly name and description"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]) or len(fields["name"]) > 64:
        return ["invalid skill name"]
    if fields["name"] != path.parent.name:
        return ["skill folder and name differ"]
    description = fields["description"]
    if not 1 <= len(description) <= 1024 or any(c in description for c in "<>"):
        return ["invalid skill description"]
    if ": " in description or description.startswith(("[", "{", "!", "*", "&")):
        return ["description must be a plain YAML string in this validator"]
    return []


def check(root):
    errors = []
    original = root / "source/original-methodology.md"
    if not original.exists():
        errors.append("original-methodology.md missing")
    else:
        raw = original.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != ORIGINAL_BLOB:
            errors.append(f"original blob mismatch: {blob}")
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for destination in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            destination = destination.strip().strip("<>")
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination) or destination.startswith("#"):
                continue
            destination = unquote(destination.split("#")[0])
            if destination and not (path.parent / destination).exists():
                errors.append(f"{path.relative_to(root)}: broken link {destination}")
    skill = root / ".agents/skills/raid-events"
    errors.extend(check_skill(skill / "SKILL.md"))
    required = ["SKILL.md", "references/tools-and-examples.md",
                "references/case-studies/perfected-guillotine-invulnerable.md",
                "scripts/compare_results.py", "scripts/extract_action.py", "scripts/build_route.py"]
    for relative in required:
        if not (skill / relative).is_file():
            errors.append(f"missing skill resource: {relative}")
    try:
        compare(json.loads((skill / "assets/guillotine-observations.json").read_text(encoding="utf-8")))
        validate(json.loads((skill / "assets/example-timeline.json").read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    return errors


def main():
    root = Path(__file__).resolve().parents[4]
    errors = check(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("OK: skill frontmatter, internal file links, original Git blob, resources and fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
