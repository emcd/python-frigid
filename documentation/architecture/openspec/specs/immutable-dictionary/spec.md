# Immutable Dictionary

## Purpose
To provide an immutable dictionary type similar to `dict` that prevents modifications after creation, ensuring data integrity for configuration objects and shared state.

## Requirements

### Requirement: Standard Immutable Dictionary
The system SHALL provide an immutable dictionary type that supports all standard read operations but raises exceptions on any modification attempt.

Priority: Critical

#### Scenario: Creation and Read Access
- **WHEN** a `Dictionary` is created with initial data
- **THEN** it can be accessed using standard dict read methods (`__getitem__`, `get`, `keys`, `values`, `items`, `__len__`, `__contains__`)
- **AND** it preserves insertion order
- **AND** it supports equality comparison with other mappings

#### Scenario: Mutation Attempt
- **WHEN** a user attempts to modify the `Dictionary` (set item, delete item, update, clear, pop)
- **THEN** the operation raises `EntryImmutability` exception
- **AND** the dictionary content remains unchanged

### Requirement: Set Operations on Dictionaries
The system SHALL support set-like operations (`|`, `&`) for combining immutable dictionaries.

Priority: High

#### Scenario: Union Operation
- **WHEN** the union operator (`|`) is used between two dictionaries
- **THEN** a new `Dictionary` is returned containing combined entries
- **AND** if keys conflict, an `EntryImmutability` exception is raised (unlike standard dict update which overwrites)

#### Scenario: Intersection Operation
- **WHEN** the intersection operator (`&`) is used between a `Dictionary` and another mapping or set
- **THEN** a new `Dictionary` is returned containing only keys present in both operands
- **AND** for mapping operands, values must also match

### Requirement: Dictionary with Validation
The system SHALL provide a dictionary variant that validates entries upon initialization using a supplied validator function.

Priority: High

#### Scenario: Validation Success
- **WHEN** a `ValidatorDictionary` is initialized with a validator and valid data
- **THEN** the dictionary is created successfully
- **AND** it behaves like a standard `Dictionary`

#### Scenario: Validation Failure
- **WHEN** a `ValidatorDictionary` is initialized with data that fails validation
- **THEN** an `EntryInvalidity` exception is raised
- **AND** the dictionary is not created
