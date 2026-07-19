# Class System

## Purpose

To define the metaclasses, base classes, and decorators that enable creation
of user-defined classes with immutable instances. Covers standard classes,
dataclasses, abstract base classes, protocols, and selective mutability.

## Requirements

### Requirement: Standard Metaclass

The system MUST provide a metaclass (`Class`) for creating classes where
instance attributes are immutable after `__init__` completes.

Priority: Critical

#### Scenario: Defining an immutable class
- **WHEN** a class is defined with `metaclass=Class`
- **THEN** instances MUST have immutable attributes after initialization

#### Scenario: Assigning during init
- **WHEN** attributes are assigned within `__init__`
- **THEN** assignment MUST succeed

#### Scenario: Assigning after init
- **WHEN** an attribute is assigned after `__init__` completes
- **THEN** `AttributeImmutability` MUST be raised

### Requirement: Dataclass Metaclass

The system MUST provide a metaclass (`Dataclass`) for dataclasses with
immutable instances, compatible with the `@dataclass` decorator.

Priority: High

#### Scenario: Defining an immutable dataclass
- **WHEN** a class is decorated with `@dataclass` and uses
  `metaclass=Dataclass`
- **THEN** the class MUST behave as a dataclass
- **AND** instances MUST have immutable fields after initialization

### Requirement: Mutable Dataclass Metaclass

The system MUST provide a metaclass (`DataclassMutable`) for dataclasses
where instance attributes are mutable.

Priority: Medium

#### Scenario: Defining a mutable dataclass
- **WHEN** a class uses `metaclass=DataclassMutable`
- **THEN** instances MUST allow attribute modification

### Requirement: Abstract Base Class Metaclass

The system MUST provide a metaclass (`AbstractBaseClass`) for abstract base
classes with immutable instances.

Priority: High

#### Scenario: Defining an immutable ABC
- **WHEN** a class uses `metaclass=AbstractBaseClass`
- **THEN** the class MUST support abstract methods
- **AND** instances MUST have immutable attributes

### Requirement: Protocol Metaclasses

The system MUST provide metaclasses for protocol classes and protocol
dataclasses, supporting both immutable and mutable variants.

Priority: Medium

#### Scenario: Defining an immutable protocol
- **WHEN** a class uses `metaclass=ProtocolClass` with `typing.Protocol`
- **THEN** the class MUST behave as a protocol
- **AND** instances MUST have immutable attributes

#### Scenario: Defining a mutable protocol
- **WHEN** a class uses `metaclass=ProtocolClass` with
  `instances_mutables='*'`
- **THEN** instances MUST allow attribute modification

#### Scenario: Defining an immutable protocol dataclass
- **WHEN** a class uses `metaclass=ProtocolDataclass` with
  `typing.Protocol`
- **THEN** the class MUST behave as a protocol dataclass
- **AND** instances MUST have immutable attributes

#### Scenario: Defining a mutable protocol dataclass
- **WHEN** a class uses `metaclass=ProtocolDataclassMutable` with
  `typing.Protocol`
- **THEN** instances MUST allow attribute modification

### Requirement: Base Classes

The system MUST provide ready-to-use base classes: `Object`, `ObjectMutable`,
`DataclassObject`, `DataclassObjectMutable`, `Protocol`, `ProtocolMutable`,
`DataclassProtocol`, and `DataclassProtocolMutable`.

Priority: High

#### Scenario: Using Object base class
- **WHEN** a class inherits from `Object`
- **THEN** instances MUST have immutable attributes after initialization

#### Scenario: Using ObjectMutable base class
- **WHEN** a class inherits from `ObjectMutable`
- **THEN** instance attributes MUST be mutable

### Requirement: Decorator for Standard Behaviors

The system MUST provide a `with_standard_behaviors` decorator that makes
any class's instances immutable after initialization.

Priority: Critical

#### Scenario: Decorating a class
- **WHEN** `@with_standard_behaviors` is applied to a class
- **THEN** instances MUST have immutable attributes after initialization

#### Scenario: Decorating with mutable attributes
- **WHEN** `@with_standard_behaviors(mutables=...)` specifies mutable
  attributes
- **THEN** those attributes MUST remain mutable
- **AND** other attributes MUST be immutable

### Requirement: Decorator for Dataclass Behaviors

The system MUST provide a `dataclass_with_standard_behaviors` decorator
for making dataclass instances immutable.

Priority: High

#### Scenario: Decorating a dataclass
- **WHEN** `@dataclass_with_standard_behaviors` is applied to a dataclass
- **THEN** instances MUST have immutable fields after initialization

### Requirement: Selective Mutability

The system MUST support declaring specific attributes as mutable while
maintaining immutability for all other attributes. Frigid accepts mutables
specifiers (names, compiled regexes, predicates, or the wildcard `'*'`)
and delegates matching to classcore.

Priority: High

#### Scenario: Named mutable attributes
- **WHEN** a class specifies mutable attributes by exact name
- **THEN** those attributes MUST be modifiable after initialization
- **AND** all other attributes MUST remain immutable

#### Scenario: Regex-matched mutable attributes
- **WHEN** a class specifies mutable attributes by compiled regex pattern
- **THEN** attributes whose names match the pattern MUST be mutable
- **AND** non-matching attributes MUST remain immutable

#### Scenario: Predicate-matched mutable attributes
- **WHEN** a class specifies mutable attributes by predicate function
- **THEN** attributes for which the predicate returns `True` MUST be mutable
- **AND** other attributes MUST remain immutable

#### Scenario: Wildcard mutability
- **WHEN** `instances_mutables='*'` is specified
- **THEN** all instance attributes MUST be mutable

### Requirement: Attribute Concealment

The system MUST delegate `dir()` filtering to classcore, which conceals
internal attributes (those matching the package-specific naming pattern)
from the public interface.

Priority: Medium

#### Scenario: Concealed attributes excluded from dir
- **WHEN** a user calls `dir()` on a frigid object
- **THEN** internal attributes (e.g., `_frigid_*_`) MUST NOT appear

#### Scenario: Concealment delegated to classcore
- **WHEN** a frigid class is constructed via the class factory
- **THEN** classcore's concealment mechanism MUST be applied
