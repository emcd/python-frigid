# Immutable Classes

## Purpose
To provide mechanisms (metaclasses and decorators) for creating classes with immutable instances, supporting both standard classes and dataclasses.

## Requirements

### Requirement: Metaclass for Immutable Classes
The system SHALL provide metaclasses that enforce immutability on instances of classes, dataclasses, abstract base classes, and protocols.

Priority: Critical

#### Scenario: Immutable Class Definition
- **WHEN** a class uses `metaclass=Class`
- **THEN** instances of that class are immutable after `__init__` completes
- **AND** setting attributes in `__init__` is allowed

#### Scenario: Immutable Dataclass Definition
- **WHEN** a class uses `metaclass=Dataclass`
- **THEN** it behaves as a frozen dataclass
- **AND** it supports standard dataclass features

### Requirement: Decorator for Immutable Classes
The system SHALL provide decorators to apply immutability behavior to existing classes without changing their metaclass hierarchy.

Priority: Critical

#### Scenario: Standard Behavior Decorator
- **WHEN** a class is decorated with `@with_standard_behaviors`
- **THEN** its instances become immutable
- **AND** it preserves existing class behavior and inheritance

#### Scenario: Dataclass Decorator
- **WHEN** a class is decorated with `@dataclass_with_standard_behaviors`
- **THEN** it is converted to a dataclass
- **AND** its instances are immutable

### Requirement: Selective Mutability
The system SHALL support marking specific attributes as mutable within an otherwise immutable class.

Priority: High

#### Scenario: Mutable Attributes
- **WHEN** a class defines `instances_mutables` (via metaclass argument or decorator)
- **THEN** attributes listed in `instances_mutables` can be modified
- **AND** all other attributes remain immutable

#### Scenario: Wildcard Mutability
- **WHEN** `instances_mutables` is set to `'*'`
- **THEN** all instance attributes are mutable
- **BUT** class attributes may still be protected
