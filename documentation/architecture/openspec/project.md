# Project Context

## Purpose
This project provides a Python library for **immutable data structures** - collections and objects which cannot be modified after creation. It aims to offer drop-in replacements for mutable built-in types (like `dict` and `SimpleNamespace`) and mechanisms to make arbitrary classes immutable, enhancing safety and predictability in Python programs while maintaining compatibility with standard Python idioms.

## Tech Stack
- **Language**: Python >= 3.10
- **Build System**: Hatch
- **Testing**: Pytest, Coverage
- **Linting & Formatting**: Ruff, Isort
- **Type Checking**: Pyright
- **Documentation**: Sphinx (with Dynadoc)
- **Changelog**: Towncrier

## Project Conventions

### Code Style
- **Linter/Formatter**: Strict adherence to `Ruff` configuration (line length 79).
- **Imports**: Organized by `isort` and centralized via the `__` subpackage.
- **Typing**: Static typing checked by `Pyright`.
- **Docstrings**: Uses `dynadoc` fragments for consistency.
- **Naming**: Follows standard Python conventions, with internal implementations often suffixed or using specific patterns (e.g., `_data_`).

### Architecture Patterns
For detailed architectural documentation, see:
- [System Overview](../summary.rst)
- [Filesystem Organization](../filesystem.rst)

**Key Patterns:**
- **Centralized Imports**: Uses a `sources/frigid/__` subpackage as a central hub for internal and external dependencies.
- **Wrapper Pattern**: Public classes often wrap internal implementations (e.g., `Dictionary` wraps `ImmutableDictionary`).
- **Delegation**: Delegates core class creation and protection logic to the `classcore` library.
- **Initialization Window**: Allows mutation during `__init__` before enforcing immutability.

### Testing Strategy
See [Test Plans](../testplans/index.rst).

- **Structure**: Tests mirror the source package structure.
- **Coverage**: Targets >95% line coverage and 100% public API coverage.
- **Doctests**: Examples in documentation are tested.
- **Markers**: Uses `slow` marker for long-running tests.

### Git Workflow
- **Pre-commit**: Uses pre-commit hooks for validation.
- **Pull Requests**: Changes are submitted via PRs.
- **OpenSpec**: Follows the OpenSpec workflow for spec-driven development (see `AGENTS.md` in this directory).

## Domain Context
- **Immutability**: The core domain is preventing state modification after initialization.
- **Practical Immutability**: Acknowledges that Python allows circumvention (e.g., via `object.__setattr__`), so the goal is safety against accidental modification, not absolute security.
- **Metaprogramming**: Heavy use of metaclasses and decorators to enforce behaviors.

## Important Constraints
- **Python Version**: Must support Python 3.10 and newer.
- **Performance**: Wrappers should introduce minimal overhead.
- **Compatibility**: Must work with `dataclasses` and other standard Python features.

## External Dependencies
- **absence**: Sentinel values.
- **classcore**: Class factories and attribute protection.
- **dynadoc**: Dynamic documentation generation.
- **typing-extensions**: For compatibility.
