# Immutability Enforcement

## Purpose

To define the cross-cutting mechanisms by which frigid enforces immutability
across all data structures, classes, and modules. This capability covers the
initialization window, behavioral flags, protection activation, and the
delegation pattern to classcore.

## Requirements

### Requirement: Initialization Window

The system MUST allow attribute and entry assignment during `__init__` and
`__post_init__`, then activate protection after initialization completes.

Priority: Critical

#### Scenario: Assignment during initialization
- **WHEN** attributes are assigned within `__init__` or `__post_init__`
- **THEN** assignment MUST succeed without raising exceptions

#### Scenario: Assignment after initialization
- **WHEN** an attribute is assigned after `__init__` completes
- **THEN** `AttributeImmutability` MUST be raised

#### Scenario: Dictionary entry assignment during initialization
- **WHEN** entries are set during dictionary `__init__`
- **THEN** assignment MUST succeed without raising exceptions

#### Scenario: Dictionary entry assignment after initialization
- **WHEN** an entry is set after dictionary `__init__` completes
- **THEN** `EntryImmutability` MUST be raised

### Requirement: Behavioral Flags

The system MUST use a behavioral flags mechanism to track immutability state,
where the presence of an `'immutability'` flag indicates that protection is
active.

Priority: High

#### Scenario: Flag absent during initialization
- **WHEN** an object is being initialized
- **THEN** the `'immutability'` flag MUST NOT be present in the behaviors set

#### Scenario: Flag present after initialization
- **WHEN** initialization completes
- **THEN** the `'immutability'` flag MUST be present in the behaviors set

### Requirement: Delegation to classcore

The system MUST delegate core immutability enforcement to
`classcore.standard.class_factory`, providing frigid-specific configuration
via partial application.

Priority: High

#### Scenario: Class factory configuration
- **WHEN** a metaclass is created using `_class_factory`
- **THEN** it MUST pass `attributes_namer`, `dynadoc_configuration`, and
  `error_class_provider` to classcore

#### Scenario: Protection enforcement
- **WHEN** classcore enforces attribute protection
- **THEN** frigid's `AttributeImmutability` exception MUST be raised for
  violations

### Requirement: Practical Immutability

The system MUST document that immutability can be circumvented by users with
intermediate Python knowledge (e.g., `object.__setattr__`), and that the
library provides practical immutability for normal usage, not security
against determined circumvention.

Priority: Medium

#### Scenario: Documentation includes caveat
- **WHEN** a user reads the package documentation
- **THEN** they MUST find a note explaining the practical nature of
  immutability enforcement

### Requirement: Delegation of Concealment

The system MUST delegate attribute concealment (`dir()` filtering) to
classcore, ensuring internal attributes are hidden from the public
interface without frigid reimplementing the concealment mechanism.

Priority: Medium

#### Scenario: Concealment via class factory
- **WHEN** a frigid class is constructed via `_class_factory`
- **THEN** classcore's concealment mechanism MUST be applied automatically
