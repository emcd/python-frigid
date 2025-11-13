.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
System Overview
*******************************************************************************

Frigid is a Python library that provides immutable data structures and class
behaviors through a layered architecture. The system enforces immutability
at multiple levels - from low-level dictionary implementations to high-level
class decorators - while maintaining compatibility with Python's standard
library patterns and third-party tools like dataclasses.

Purpose and Scope
===============================================================================

The library addresses the need for immutable data structures in Python by:

* Providing drop-in replacements for mutable built-in types (dict, namespace)
* Enabling conversion of arbitrary classes to immutable variants
* Supporting selective mutability for gradual adoption
* Maintaining type safety and comprehensive documentation

The library does not attempt to make immutability completely unbreakable
(which is impossible in Python), but instead provides practical immutability
that integrates naturally with Python's idioms and existing code.

Major Components
===============================================================================

The system is organized into distinct layers that build upon each other:

Public API Layer
-------------------------------------------------------------------------------

**dictionaries.py**
  Immutable dictionary implementations with two variants:

  - ``Dictionary``: Standard immutable dictionary similar to dict but frozen
  - ``ValidatorDictionary``: Dictionary with validation on initialization
  - Provides set operations (union, intersection) not available on MappingProxyType

**namespaces.py**
  Immutable namespace objects similar to ``types.SimpleNamespace`` but with
  frozen attributes after creation.

**classes.py**
  Metaclasses and decorators for creating immutable classes:

  - Metaclasses (Class, Dataclass, AbstractBaseClass, ProtocolClass, etc.)
  - Base classes (Object, DataclassObject, Protocol variants)
  - Decorators (with_standard_behaviors, dataclass_with_standard_behaviors)

**modules.py**
  Immutable module types and utilities for freezing module-level constants
  after initialization.

**sequences.py**
  Utility functions for creating immutable sequences, primarily the ``one()``
  function for single-item tuples.

**exceptions.py**
  Exception hierarchy for immutability violations:

  - ``AttributeImmutability``: Raised when modifying immutable attributes
  - ``EntryImmutability``: Raised when modifying immutable dictionary entries
  - ``EntryInvalidity``: Raised when validation fails

**installers.py**
  Convenience utilities for installing frigid functions into Python builtins.

Core Implementation Layer
-------------------------------------------------------------------------------

Located in the ``__`` subpackage (internal implementation):

**ImmutableDictionary** (``__/dictionaries.py``)
  The foundational immutable dictionary class that all other dictionary-based
  structures build upon. Subclasses ``dict`` and uses behavioral flags to
  enforce immutability after initialization.

**imports.py** (``__/imports.py``)
  Centralized import hub providing all external dependencies through a single
  namespace. Primary dependencies include classcore, dynadoc, absence, and
  typing_extensions.

**nomina.py** (``__/nomina.py``)
  Type aliases, type variables, and naming utilities used throughout the
  package.

**doctab.py** (``__/doctab.py``)
  Documentation fragments table for dynamic documentation generation via
  dynadoc.

**exceptions.py** (``__/exceptions.py``)
  Internal exception classes used by the implementation layer.

Foundation Dependencies
-------------------------------------------------------------------------------

**classcore**
  Provides the core class factory mechanism and attribute protection system.
  Frigid delegates most low-level immutability enforcement to classcore's
  ``standard`` module while providing higher-level API and configuration.

**dynadoc**
  Enables dynamic documentation generation using reusable fragments. All
  classes define ``_dynadoc_fragments_`` attributes referencing documentation
  strings from the doctab.

**absence**
  Provides the ``absent`` sentinel value for distinguishing missing values
  from ``None`` in optional parameters.

Component Relationships
===============================================================================

Architecture Layers
-------------------------------------------------------------------------------

The system follows a clear layered architecture:

::

    ┌─────────────────────────────────────────────────────────────┐
    │  Public API                                                 │
    │  (Dictionary, Namespace, Object, decorators)                │
    └─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  Core Implementation (__/)                                  │
    │  (ImmutableDictionary, type aliases, doc fragments)         │
    └─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────────────────────────────────────────┐
    │  Foundation Libraries                                       │
    │  (classcore, dynadoc, absence)                              │
    └─────────────────────────────────────────────────────────────┘

Dependency Flow
-------------------------------------------------------------------------------

All modules follow the ``__`` import pattern:

1. Public modules import from ``. import __``
2. The ``__`` package provides centralized access to external dependencies
3. Configuration flows from public API through to classcore via partial application
4. Runtime checks flow from classcore back through implementation to user code

Key dependencies between components:

* ``dictionaries.py`` → ``classes.py`` (uses AbstractBaseClass metaclass)
* ``namespaces.py`` → ``classes.py`` (uses Object base class)
* ``modules.py`` → ``classes.py`` (uses Module metaclass)
* All components → ``__`` (centralized imports and utilities)
* ``classes.py`` → ``classcore.standard`` (core class factory)

Data Flow Patterns
===============================================================================

Initialization Flow
-------------------------------------------------------------------------------

Immutable objects follow a consistent initialization pattern:

1. Object creation begins with standard Python ``__new__``
2. During ``__init__``, attributes/entries can be freely set
3. After ``__init__`` completes, protection is activated
4. Subsequent modification attempts raise immutability exceptions

For ``ImmutableDictionary``:

::

    __init__ starts
         ↓
    Set entries in dict (immutability not active)
         ↓
    Add 'immutability' flag to _behaviors_
         ↓
    __init__ completes
         ↓
    Future __setitem__/__delitem__ check flag and raise exceptions

For classes using metaclasses:

::

    User class definition
         ↓
    Metaclass __new__ with classcore.standard.class_factory
         ↓
    Instance __init__ (attributes can be set)
         ↓
    Protection activated via __setattr__/__delattr__ overrides
         ↓
    Future modifications raise AttributeImmutability

Operation Flow
-------------------------------------------------------------------------------

Dictionary operations (union, intersection) maintain immutability:

1. User invokes operation: ``dict1 | dict2``
2. Operation method computes new data
3. Method calls ``with_data()`` to create new instance
4. New instance has same type and validator (if applicable)
5. Returns new immutable dictionary

Class Creation Flow
-------------------------------------------------------------------------------

When using decorators or metaclasses:

::

    User defines class with metaclass or decorator
         ↓
    Metaclass or decorator invokes _class_factory (partial)
         ↓
    classcore.standard.class_factory receives configuration:
      - attributes_namer (calculate_attrname)
      - dynadoc_configuration
      - error_class_provider
      - protection/concealment behaviors
         ↓
    Returns configured class with immutability enforcement
         ↓
    User creates instances with standard constructor
         ↓
    classcore enforces attribute protection after __init__

Key Architectural Patterns
===============================================================================

Wrapper Pattern
-------------------------------------------------------------------------------

Public classes wrap internal implementations:

* ``Dictionary`` wraps ``ImmutableDictionary`` stored in ``_data_`` attribute
* ``ValidatorDictionary`` extends ``Dictionary`` with ``_validator_`` attribute
* ``Namespace`` uses ``ImmutableDictionary`` for ``__dict__``

This separation provides:

* Clean public API distinct from implementation details
* Flexibility to change implementation without breaking API
* Support for subclassing and specialization

Delegation Pattern
-------------------------------------------------------------------------------

Frigid delegates core functionality to classcore rather than reimplementing
immutability mechanisms. This provides:

* Reduced code duplication
* Leveraging battle-tested implementation
* Consistent behavior with other classcore-based packages
* Focus on user-facing API and documentation

Configuration via Partial Application
-------------------------------------------------------------------------------

Class factories use ``functools.partial`` to bind frigid-specific configuration:

.. code-block:: python

    _class_factory = partial(
        ccstd.class_factory,
        attributes_namer=calculate_attrname,
        dynadoc_configuration=DynadocConfiguration(...),
        error_class_provider=_provide_error_class,
    )

This pattern enables:

* Reusable configuration across multiple metaclasses
* Clear separation of frigid customization from classcore mechanics
* Type-safe configuration that fails at import time, not runtime

Centralized Import Hub Pattern
-------------------------------------------------------------------------------

The ``__`` subpackage provides consistent access to dependencies:

* All modules use ``from . import __``
* Single source of truth for external dependencies
* Easy refactoring of dependencies
* Reduced import overhead through centralization

Template Method Pattern
-------------------------------------------------------------------------------

Abstract methods enable customization in subclasses:

* ``Dictionary.with_data()`` - creates new instance with different data
* Subclasses override to maintain type and behavior
* Enables operations like union/intersection to return correct types

Behavioral Flags Pattern
-------------------------------------------------------------------------------

``ImmutableDictionary`` uses a ``_behaviors_`` set to track state:

* During ``__init__``, 'immutability' not in set (modifications allowed)
* After ``__init__``, 'immutability' added to set (modifications blocked)
* Methods check flag before allowing operations
* Provides clear initialization window without complex state tracking

Quality Attributes
===============================================================================

Maintainability
-------------------------------------------------------------------------------

* Clear layered architecture separates concerns
* Delegation to classcore reduces maintenance burden
* Centralized imports simplify dependency management
* Comprehensive documentation via dynadoc

Usability
-------------------------------------------------------------------------------

* Familiar API similar to built-in types
* Multiple access patterns (metaclasses, decorators, direct instantiation)
* Clear exception messages for violations
* Gradual adoption via selective mutability

Compatibility
-------------------------------------------------------------------------------

* Works with dataclasses and other decorators
* Compatible with protocols and abstract base classes
* Supports pickling and standard Python introspection
* Respects existing Python conventions

Performance
-------------------------------------------------------------------------------

* Centralized imports reduce per-module import overhead
* Delegation to classcore leverages optimized C code where available
* Minimal runtime overhead beyond Python's standard attribute access
* No runtime code generation or bytecode manipulation

System Constraints
===============================================================================

Python Language Limitations
-------------------------------------------------------------------------------

True immutability is impossible in Python:

* Anyone with intermediate knowledge can circumvent protections
* ``object.__setattr__`` can bypass custom ``__setattr__``
* Direct manipulation of ``__dict__`` possible in some cases
* Reflection and introspection expose internal state

The library provides practical immutability for normal usage, not security
against determined circumvention.

Initialization Window Requirement
-------------------------------------------------------------------------------

Objects must support normal Python initialization:

* ``__init__`` must be able to set attributes
* Dataclass initialization requires attribute assignment
* Protection activates only after ``__init__`` completes
* Brief window where object is technically mutable

Compatibility with Third-Party Tools
-------------------------------------------------------------------------------

Must work with existing Python ecosystem:

* Dataclasses require specific initialization patterns
* Pickling requires certain attributes to be accessible
* Introspection tools expect standard Python semantics
* Documentation tools need readable docstrings and signatures