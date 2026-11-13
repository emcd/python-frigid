# Project Guidance

Project-owned knowledge the generated `AGENTS.md` entrypoint must not own.
Structured tracking stays in `nb`.

## Purpose

Immutable data structures for Python — collections and classes which cannot be
modified after creation. The public API lives in `sources/frigid/`; internal
machinery under `sources/frigid/__/` delegates attribute concealment and
immutability behaviors to Classcore rather than reimplementing them.

## Tech Stack

- Python 3.12 and later, CPython only. PyPy is not supported.
- Classcore (class factories, attribute protection, internal-name grammar),
  Dynadoc (docstring generation), Absence (sentinel values).
- Hatch for environments, versioning, and quality gates.
- Towncrier for changelog fragments.
- Sphinx for documentation, including doctests. Doctests are run through
  Sphinx, not Pytest, because Pytest mutates the `_` attribute on protected
  modules.

## Notes

- **Never import from a module whose name starts with an underscore.** This
  holds across package boundaries and for our own `frigid.__` internals. The
  test suite violates it in places; tracked as `issues/tests/3`.
- Prefer the shared Classcore surface over local mirrors. A drifted local copy
  of the ABC and typing mutables sets caused the CPython 3.15 typing-dunder
  refusal; the attribute-name calculator is imported from
  `classcore.standard.nomina` for the same reason.
- **Release process**: `.auxiliary/agents/standards/releases-python.md`, with
  news fragments under `.auxiliary/data/towncrier`. Types are `enhance`,
  `notify`, `remove`, `repair`. Do not commit or push without explicit user
  approval.
- **Validation**: `hatch --env develop run linters`, `testers`, `docsgen`.
- **`nb` folder taxonomy**: `<issue-type>/<component>`, maximum depth 2. Issue
  types are `todos/`, `coordination/`, `issues/`, `decisions/`. Component
  names in use: `classes`, `dictionaries`, `modules`, `nomina`, `sequences`,
  `tests`, `general`. Cross-component work goes in `coordination/general`;
  per-component rolling handoffs in `coordination/<component>`.
