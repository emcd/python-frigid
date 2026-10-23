# Utilities

## Purpose
To provide utility functions that enhance readability and convenience when working with immutable structures.

## Requirements

### Requirement: Sequence Utilities
The system SHALL provide utilities for creating immutable sequences more readably.

Priority: Medium

#### Scenario: Single Item Tuple
- **WHEN** `one(x)` is called
- **THEN** it returns a tuple containing exactly one element `(x,)`
- **AND** it is typed correctly

### Requirement: Builtins Installation
The system SHALL provide an optional mechanism to install utilities into builtins.

Priority: Low

#### Scenario: Installation
- **WHEN** the installer function is called
- **THEN** utilities like `one` are available in the builtins namespace
- **AND** this is opt-in only
