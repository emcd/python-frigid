# Exception Hierarchy

## Purpose

To define the exception hierarchy for handling violations of immutability
and validation constraints. Exceptions inherit from both frigid's hierarchy
and appropriate Python built-in exceptions for dual catchability.

## Requirements

### Requirement: Exception Hierarchy Root

The system MUST provide an exception hierarchy rooted in `Omniexception`
(base for all frigid exceptions) and `Omnierror` (base for error conditions).

Priority: Critical

#### Scenario: Catching all frigid exceptions
- **WHEN** a user catches `Omniexception`
- **THEN** all exceptions raised by the package MUST be caught

#### Scenario: Catching all frigid errors
- **WHEN** a user catches `Omnierror`
- **THEN** all error exceptions raised by the package MUST be caught

### Requirement: Attribute Immutability Exception

The system MUST provide `AttributeImmutability` (inherits `Omnierror` and
`AttributeError`) raised when attempting to modify or delete an immutable
attribute.

Priority: Critical

#### Scenario: Catching via frigid hierarchy
- **WHEN** a user catches `AttributeImmutability`
- **THEN** attribute modification violations MUST be caught

#### Scenario: Catching via built-in hierarchy
- **WHEN** a user catches `AttributeError`
- **THEN** `AttributeImmutability` MUST also be caught

#### Scenario: Exception message includes context
- **WHEN** `AttributeImmutability` is raised
- **THEN** the message MUST include the attribute name and target

### Requirement: Entry Immutability Exception

The system MUST provide `EntryImmutability` (inherits `Omnierror` and
`TypeError`) raised when attempting to modify or delete an immutable
dictionary entry.

Priority: Critical

#### Scenario: Catching via frigid hierarchy
- **WHEN** a user catches `EntryImmutability`
- **THEN** dictionary entry modification violations MUST be caught

#### Scenario: Catching via built-in hierarchy
- **WHEN** a user catches `TypeError`
- **THEN** `EntryImmutability` MUST also be caught

#### Scenario: Exception message includes key
- **WHEN** `EntryImmutability` is raised
- **THEN** the message MUST include the entry key

### Requirement: Entry Invalidity Exception

The system MUST provide `EntryInvalidity` (inherits `Omnierror` and
`ValueError`) raised when a dictionary entry fails validation.

Priority: High

#### Scenario: Catching via frigid hierarchy
- **WHEN** a user catches `EntryInvalidity`
- **THEN** validation failures MUST be caught

#### Scenario: Catching via built-in hierarchy
- **WHEN** a user catches `ValueError`
- **THEN** `EntryInvalidity` MUST also be caught

#### Scenario: Exception message includes key and value
- **WHEN** `EntryInvalidity` is raised
- **THEN** the message MUST include the entry key and value
