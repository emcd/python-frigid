# Builtins Integration

## Purpose

To define the opt-in mechanism for exposing frigid utility functions as Python
builtins, allowing users to call them without explicit imports. This capability
covers the `install` function and its configuration options.

## Requirements

### Requirement: Opt-In Builtins Installation

The system MUST provide an `install` function that optionally adds the
`one` tuple constructor to Python's builtins namespace. The function MUST
default to installing under the name `one`.

Priority: Low

#### Scenario: Default installation
- **WHEN** `install()` is called with no arguments
- **THEN** `one` MUST be available as a builtin function
- **AND** `one(42)` MUST return `(42,)`

#### Scenario: Custom name installation
- **WHEN** `install('single')` is called with a custom name
- **THEN** the function MUST be available under the given name in builtins
- **AND** `single(42)` MUST return `(42,)`

#### Scenario: Skipping installation
- **WHEN** `install(None)` is called
- **THEN** the function MUST return without adding or replacing any builtin
