# markdown-link-auditor

Audit relative file links and image paths in Markdown documentation without network access.

A small, dependency-free Python project designed to be useful on its own and easy
for coding agents to understand. Runs locally; no API keys or services required.

## Quick start

Requires Python 3.11 or newer. From the repository root:

```sh
python -m link_auditor examples/docs
python -m unittest discover -s tests -v
```

Optional installation in a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
markdown-link-auditor --help
```

## Behavior and limits

Checks inline links and images, optional quoted titles and angle-bracket paths.
Skips fenced code, simple inline code, external URLs and fragment-only links.
URL escapes are decoded; fragments and queries are ignored. Root-relative paths
resolve within the supplied documentation root. Escaping that root is an issue.
Symlinked source files are skipped; target symlinks are resolved for containment.
This is a deliberately limited parser: reference-style links, HTML, nested
parentheses, complex code spans and heading-anchor validation are unsupported.
Exit codes: 0 no issues, 1 broken/outside-root links, 2 invalid input or I/O error.

## Layout

- `link_auditor/core.py`: public functions and command-line interface.
- `tests/`: unit and command-line regression tests.
- `examples/`: small, synthetic inputs safe to share publicly.
- `AGENTS.md`: orientation and working conventions for coding agents.
- `docs/architecture.md`: data flow and extension points.

## Possible next steps

- Add reference-style link support.
- Validate heading anchors.
- Add ignore patterns for generated documentation.

These are suggestions for future work, not implemented features.

## Development

Tests use the Python standard library. The CI workflow runs them on Python 3.11
and 3.12. Keep changes focused and add regression tests for behavior changes.
The project is intentionally small; it does not claim production readiness.

## License

MIT. See [LICENSE](LICENSE).
