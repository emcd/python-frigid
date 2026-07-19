# Immutable Collections

## Purpose

To define the immutable collection types provided by frigid: dictionaries
(with validation), namespaces, and sequences. These types enforce complete
immutability after creation, unlike `types.MappingProxyType` which is a view
over a mutable dictionary.

## Requirements

### Requirement: Abstract Dictionary Interface

The system MUST provide an abstract base class defining the immutable
dictionary interface, requiring implementations to provide `__getitem__`,
`__iter__`, and `__len__`.

Priority: Critical

#### Scenario: Incomplete implementation
- **WHEN** a subclass does not implement all abstract methods
- **THEN** instantiation MUST raise `TypeError`

### Requirement: Basic Immutable Dictionary

The system MUST provide a standard immutable dictionary (`Dictionary`) that
prevents any modification or removal of entries after creation.

Priority: Critical

#### Scenario: Retrieving entries
- **WHEN** a user accesses an existing key
- **THEN** the associated value MUST be returned

#### Scenario: Adding entries after creation
- **WHEN** a user attempts to add a new key-value pair
- **THEN** `EntryImmutability` MUST be raised

#### Scenario: Modifying existing entries
- **WHEN** a user attempts to update the value of an existing key
- **THEN** `EntryImmutability` MUST be raised
- **AND** the original value MUST remain unchanged

#### Scenario: Removing entries
- **WHEN** a user attempts to delete an existing key
- **THEN** `EntryImmutability` MUST be raised
- **AND** the entry MUST remain in the dictionary

### Requirement: Validator Dictionary

The system MUST provide a dictionary (`ValidatorDictionary`) that validates
entries using a predicate function before creation, ensuring only valid data
can be stored.

Priority: High

#### Scenario: Creating with valid entries
- **WHEN** a user creates a ValidatorDictionary with entries that pass
  the predicate
- **THEN** creation MUST succeed
- **AND** all entries MUST be stored

#### Scenario: Creating with invalid entries
- **WHEN** a user attempts to create a ValidatorDictionary with an entry
  that fails the predicate
- **THEN** `EntryInvalidity` MUST be raised
- **AND** no entries MUST be stored

### Requirement: Dictionary Set Operations

The system MUST provide union (`|`) and intersection (`&`) operations on
immutable dictionaries that return new immutable dictionaries.

Priority: Medium

#### Scenario: Union with non-overlapping keys
- **WHEN** a user unions two dictionaries with no common keys
- **THEN** a new dictionary containing all entries from both MUST be returned

#### Scenario: Union with overlapping keys
- **WHEN** a user unions two dictionaries with common keys
- **THEN** `EntryImmutability` MUST be raised

#### Scenario: Intersection by mapping
- **WHEN** a user intersects a dictionary with a mapping
- **THEN** a new dictionary containing only entries with matching keys
  and values MUST be returned

#### Scenario: Intersection by key set
- **WHEN** a user intersects a dictionary with a set of keys
- **THEN** a new dictionary containing only entries with keys in the set
  MUST be returned

### Requirement: Dictionary Copy and Factory

The system MUST provide `copy()` and `with_data()` methods on immutable
dictionaries, where `copy()` returns a fresh instance and `with_data()`
creates a new instance preserving behavior (e.g., validator).

Priority: Medium

#### Scenario: Copying a dictionary
- **WHEN** a user calls `copy()` on an immutable dictionary
- **THEN** a new instance of the same type with the same data MUST be returned

#### Scenario: Creating with factory
- **WHEN** a user calls `with_data()` on a ValidatorDictionary
- **THEN** a new ValidatorDictionary with the same validator and new data
  MUST be returned

### Requirement: Immutable Namespace

The system MUST provide a namespace (`Namespace`) where all attributes are
immutable after initialization, similar to `types.SimpleNamespace`.

Priority: Critical

#### Scenario: Initializing with attributes
- **WHEN** a user creates a namespace with keyword arguments
- **THEN** the attributes MUST be accessible via dot notation

#### Scenario: Assigning new attributes after creation
- **WHEN** a user attempts to assign a new attribute on an existing namespace
- **THEN** `AttributeImmutability` MUST be raised

#### Scenario: Modifying existing attributes
- **WHEN** a user attempts to reassign an existing attribute
- **THEN** `AttributeImmutability` MUST be raised
- **AND** the original value MUST remain unchanged

#### Scenario: Deleting attributes
- **WHEN** a user attempts to delete an existing attribute
- **THEN** `AttributeImmutability` MUST be raised
- **AND** the attribute MUST remain in the namespace

#### Scenario: Multiple initialization forms
- **WHEN** a user creates a namespace from iterables, mappings, or keyword
  arguments
- **THEN** all provided attributes MUST be accessible

#### Scenario: Equality with SimpleNamespace
- **WHEN** a namespace and a SimpleNamespace have the same attributes and values
- **THEN** they MUST be considered equal

### Requirement: Single-Item Tuple Factory

The system MUST provide a `one()` function that creates a single-item tuple
from a value, as a more readable alternative to `(x,)` syntax.

Priority: Low

#### Scenario: Creating a single-item tuple
- **WHEN** a user calls `one(42)`
- **THEN** the result MUST be `(42,)`
