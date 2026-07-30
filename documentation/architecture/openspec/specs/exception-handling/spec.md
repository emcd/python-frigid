# Exception Handling

## Purpose
To provide a clear and specific exception hierarchy for identifying and handling immutability violations.

## Requirements

### Requirement: Clear Exception Hierarchy
The system SHALL provide a hierarchy of exceptions inheriting from standard Python exceptions where appropriate.

Priority: Critical

#### Scenario: Attribute Immutability Exception
- **WHEN** an attribute modification is attempted on an immutable object
- **THEN** `AttributeImmutability` is raised
- **AND** it inherits from `AttributeError`
- **AND** the message identifies the attribute and target

#### Scenario: Entry Immutability Exception
- **WHEN** a dictionary modification is attempted
- **THEN** `EntryImmutability` is raised
- **AND** it inherits from `TypeError`
- **AND** the message identifies the key

#### Scenario: Entry Invalidity Exception
- **WHEN** a validation fails in `ValidatorDictionary`
- **THEN** `EntryInvalidity` is raised
- **AND** it inherits from `ValueError`

#### Scenario: Base Exceptions
- **WHEN** catching `Omniexception` or `Omnierror`
- **THEN** it catches all library-specific exceptions
