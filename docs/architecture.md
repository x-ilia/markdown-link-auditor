# Architecture

`python -m link_auditor` delegates to `core.main`. Argument parsing and filesystem
access live at the boundary; the exported core functions own the behavior.
Results are plain Python data structures that can be serialized as JSON.

## Design decisions

- Standard library only: easy to run in a fresh agent environment.
- Explicit validation: bad input should fail predictably rather than be coerced.
- Stable ordering: examples and tests stay reproducible across machines.
- Read-only processing: input files are never modified.

## Extension strategy

Add a focused core function, test it using synthetic fixtures, then expose it via
the CLI. Keep the documented default behavior compatible where possible.

## Scope

Checks inline links and images, optional quoted titles and angle-bracket paths.
Skips fenced code, simple inline code, external URLs and fragment-only links.
URL escapes are decoded; fragments and queries are ignored. Root-relative paths
resolve within the supplied documentation root. Escaping that root is an issue.
Symlinked source files are skipped; target symlinks are resolved for containment.
This is a deliberately limited parser: reference-style links, HTML, nested
parentheses, complex code spans and heading-anchor validation are unsupported.
Exit codes: 0 no issues, 1 broken/outside-root links, 2 invalid input or I/O error.
