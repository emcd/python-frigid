# Immutable Namespace

## Purpose
To provide an immutable namespace type similar to `types.SimpleNamespace` for simple object-like access to immutable data.

## Requirements

### Requirement: Immutable Namespace Object
The system SHALL provide an immutable namespace type that allows attribute access but prevents modification after initialization.

Priority: Critical

#### Scenario: Creation and Read Access
- **WHEN** a `Namespace` is created with keyword arguments or a dictionary
- **THEN** attributes can be accessed using dot notation
- **AND** it supports equality comparison
- **AND** it provides a readable `repr` showing all attributes

#### Scenario: Mutation Attempt
- **WHEN** a user attempts to set or delete an attribute on a `Namespace` instance
- **THEN** an `AttributeImmutability` exception is raised
- **AND** the attribute remains unchanged
