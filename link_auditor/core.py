"""Check a documented subset of inline Markdown links against local files."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"!?\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s)]+))(?:\s+\"[^\"\n]*\")?\)")

def links(text: str):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for match in LINK.finditer(line):
            yield number, match.group(1) or match.group(2)

def audit(root: Path) -> list[dict]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("root must be a directory")
    issues = []
    for source in sorted(root.rglob("*.md")):
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            continue
        for line, target in links(source.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            decoded = unquote(parsed.path)
            # Root-relative links refer to this documentation root, not the host filesystem.
            destination = ((root / decoded.lstrip("/")) if decoded.startswith("/")
                           else source.parent / decoded).resolve()
            reason = None
            if not destination.is_relative_to(root):
                reason = "outside_root"
            elif not destination.exists():
                reason = "missing_target"
            if reason:
                issues.append({"source": source.relative_to(root).as_posix(),
                               "line": line, "target": target, "code": reason})
    return issues

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args(argv)
    try:
        issues = audit(args.root)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(json.dumps({"issues": issues}, indent=2, ensure_ascii=False))
    return int(bool(issues))
