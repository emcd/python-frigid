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
Product Requirements Document
*******************************************************************************

Executive Summary
===============================================================================

Frigid is a Python library that provides practical immutability for Python
data structures and classes. The library addresses the gap between Python's
mutable-by-default design and the need for immutable objects in modern
software development practices. By offering familiar APIs similar to built-in
types (dict, namespace) and flexible integration mechanisms (metaclasses,
decorators), frigid enables developers to adopt immutability gradually and
pragmatically.

The library targets Python developers who need immutable data structures for
configuration objects, value objects, thread-safe data sharing, and functional
programming patterns, while maintaining compatibility with the broader Python
ecosystem including dataclasses, protocols, and type checking tools.

Problem Statement
===============================================================================

Python's built-in data structures (dict, list, set) and user-defined classes
are mutable by default. While Python provides some immutable types (tuple,
frozenset, str), it lacks comprehensive immutable alternatives for common
use cases:

**Who experiences the problem:**

* Python developers building concurrent or distributed systems
* Teams adopting functional programming patterns
* Developers creating configuration management systems
* Library authors providing public APIs with stability guarantees
* Engineers working with shared state across threads or processes

**When and where it occurs:**

* Configuration objects that should remain constant after initialization
* Value objects that represent immutable concepts (coordinates, timestamps)
* Shared data structures accessed by multiple threads
* API responses that should not be modified by consumers
* Cache keys that must maintain consistent hash values

**Impact and consequences:**

* Unintended mutations cause hard-to-debug errors
* Race conditions in concurrent code from shared mutable state
* Cache invalidation issues from objects changing after hashing
* Defensive copying proliferates throughout codebases
* Lack of compile-time guarantees about object immutability

**Current workarounds and limitations:**

* ``types.MappingProxyType`` - read-only view but lacks set operations and
  creates indirection
* Manual ``__setattr__`` overrides - error-prone boilerplate for each class
* Converting to tuples - loses named access and type information
* Frozen dataclasses - limited to dataclasses and requires decorator
* Custom implementations - inconsistent behavior across projects

None of these solutions provide a comprehensive, ergonomic, and consistent
approach to immutability across different Python constructs.

Goals and Objectives
===============================================================================

Primary Objectives
-------------------------------------------------------------------------------

**GOAL-001: Provide drop-in immutable replacements for common built-in types**

* Success metric: Users can replace ``dict`` with ``Dictionary`` and
  ``types.SimpleNamespace`` with ``Namespace`` with minimal code changes
* Success metric: Immutable versions support all read operations of their
  mutable counterparts

**GOAL-002: Enable conversion of arbitrary classes to immutable variants**

* Success metric: Developers can make any class immutable using a decorator
  or metaclass
* Success metric: Works with dataclasses, protocols, and abstract base classes

**GOAL-003: Maintain compatibility with Python ecosystem**

* Success metric: Compatible with type checkers (mypy, pyright)
* Success metric: Works with pickle, copy, and standard introspection tools
* Success metric: Integrates with dataclasses and other decorators

**GOAL-004: Support gradual adoption**

* Success metric: Selective mutability allows specific attributes to remain
  mutable
* Success metric: Clear migration path from mutable to immutable code
* Success metric: Interoperability with mutable code without defensive copying

Secondary Objectives
-------------------------------------------------------------------------------

**GOAL-005: Provide clear error messages for immutability violations**

* Success metric: Exceptions include attribute/entry names in error messages
* Success metric: Users can quickly identify and fix violations

**GOAL-006: Minimize performance overhead**

* Success metric: Immutable operations have comparable performance to mutable
  equivalents
* Success metric: Import time and memory overhead remain minimal

**GOAL-007: Comprehensive documentation and examples**

* Success metric: All public APIs have complete documentation
* Success metric: Examples cover common use cases
* Success metric: Migration guides assist users transitioning from mutable code

Functional Requirements
===============================================================================

Immutable Dictionary
-------------------------------------------------------------------------------

**REQ-001: Standard Immutable Dictionary** (Priority: Critical)

Provide an immutable dictionary type similar to dict that prevents
modifications after creation.

Requirements:

* Initialization from iterables, mappings, and keyword arguments
* All read operations (``__getitem__``, ``get``, ``keys``, ``values``,
  ``items``, ``__len__``, ``__contains__``)
* Mutations (``__setitem__``, ``__delitem__``, ``clear``, ``pop``,
  ``popitem``, ``update``) raise immutability exceptions
* Supports equality comparison and hashing
* Preserves dict-like repr and iteration order

**REQ-002: Set Operations on Dictionaries** (Priority: High)

Support set-like operations for combining immutable dictionaries.

Requirements:

* Union operation (``|``) creates new immutable dictionary
* Intersection operation (``&``) creates new immutable dictionary
* Operations return same type as operands (subclass-aware)
* Type signatures accept both mutable and immutable dictionaries

**REQ-003: Dictionary with Validation** (Priority: High)

Provide a dictionary variant that validates entries on initialization.

Requirements:

* Accepts validator function during initialization
* Validator receives all entries and raises exception on invalid data
* Validation occurs before immutability is enforced
* Clear error messages indicate which entries failed validation

Immutable Namespace
-------------------------------------------------------------------------------

**REQ-004: Immutable Namespace Object** (Priority: Critical)

Provide an immutable namespace type similar to types.SimpleNamespace for
simple immutable objects with attribute access.

Requirements:

* Initialization from iterables, mappings, and keyword arguments
* Attribute read access (``__getattr__``)
* Attribute modifications (``__setattr__``, ``__delattr__``) raise exceptions
* Supports equality comparison
* Readable repr showing all attributes

Immutable Classes
-------------------------------------------------------------------------------

**REQ-005: Metaclass for Immutable Classes** (Priority: Critical)

Provide metaclasses for creating immutable class hierarchies.

Requirements:

* Metaclass ``Class`` for standard immutable classes
* Metaclass ``Dataclass`` for immutable dataclasses
* Metaclass ``AbstractBaseClass`` compatible with abc.ABCMeta
* Protocol metaclasses for structural typing
* Attributes can be set during ``__init__``
* Attribute protection activates after ``__init__`` completes

**REQ-006: Decorator for Immutable Classes** (Priority: Critical)

Provide decorators to make existing classes immutable without changing
inheritance.

Requirements:

* ``with_standard_behaviors`` decorator for any class
* ``dataclass_with_standard_behaviors`` combines dataclass and immutability
* Works with existing decorators (property, classmethod, staticmethod)
* Compatible with inheritance hierarchies
* Preserves type hints and docstrings

**REQ-007: Selective Mutability** (Priority: High)

Support marking specific attributes as mutable for gradual adoption.

Requirements:

* Metaclass parameter ``instances_mutables`` lists mutable attributes
* Decorator parameter ``instances_mutables`` lists mutable attributes
* Wildcard (``'*'``) allows all instance attributes to be mutable
* Class attributes remain protected by default
* Clear error messages distinguish protected vs. mutable attributes

Immutable Modules
-------------------------------------------------------------------------------

**REQ-008: Immutable Module Type** (Priority: Medium)

Provide immutable module types to prevent modification of module-level
constants.

Requirements:

* ``Module`` class extends types.ModuleType
* Module attributes cannot be modified after ``finalize_module`` call
* Integration with dynadoc for documentation generation
* Compatible with standard module importing

Utility Functions
-------------------------------------------------------------------------------

**REQ-009: Sequence Utilities** (Priority: Medium)

Provide readable utilities for creating immutable sequences.

Requirements:

* ``one(x)`` creates single-item tuple more readably than ``(x,)``
* Compatible with type checkers
* Minimal performance overhead

**REQ-010: Builtins Installation** (Priority: Low)

Support optional installation of frigid functions into builtins.

Requirements:

* Installer function adds frigid utilities to builtins
* Opt-in mechanism (not automatic)
* Clear documentation about when to use

Exception Handling
-------------------------------------------------------------------------------

**REQ-011: Clear Exception Hierarchy** (Priority: Critical)

Provide clear exception hierarchy for debugging immutability violations.

Requirements:

* ``AttributeImmutability`` for attribute violations (inherits AttributeError)
* ``EntryImmutability`` for dictionary entry violations (inherits TypeError)
* ``EntryInvalidity`` for validation failures (inherits ValueError)
* Exception messages include attribute/entry names
* Base exception classes (``Omniexception``, ``Omnierror``) for catching all
  frigid exceptions

Non-Functional Requirements
===============================================================================

Performance Requirements
-------------------------------------------------------------------------------

**NFR-001: Low Overhead**

* Import time < 100ms on standard hardware
* Immutable dictionary operations within 2x of built-in dict performance
* Attribute access on immutable objects within 1.5x of regular classes
* Memory overhead < 10% compared to mutable equivalents

**NFR-002: Scalability**

* Support dictionaries with 1M+ entries without performance degradation
* Support class hierarchies with 10+ levels of inheritance
* Minimal performance impact from attribute protection

Compatibility Requirements
-------------------------------------------------------------------------------

**NFR-003: Python Version Support**

* Support Python 3.10+ (latest stable versions)
* Follow Python's deprecation schedule for older versions
* Test against multiple Python implementations (CPython priority)

**NFR-004: Type Checking Compatibility**

* Full type hint coverage for public APIs
* Compatible with mypy, pyright, and other type checkers
* Proper generic type support for containers
* dataclass_transform decorator for dataclass metaclasses

**NFR-005: Ecosystem Integration**

* Pickle support for all immutable types
* Copy module compatibility (deepcopy, copy)
* Works with standard introspection (inspect module)
* Compatible with other decorators and metaclasses

Usability Requirements
-------------------------------------------------------------------------------

**NFR-006: API Familiarity**

* Immutable types mirror built-in type interfaces
* Method names follow Python naming conventions
* Consistent behavior with Python's data model
* Familiar initialization patterns

**NFR-007: Error Messages**

* Informative exception messages with context
* Clear indication of which attribute/entry caused violation
* Helpful suggestions for common mistakes
* Stack traces point to user code, not library internals

**NFR-008: Documentation Quality**

* Comprehensive API documentation for all public symbols
* Practical examples for each major feature
* Migration guides from common patterns
* Performance characteristics documented
* Type hints visible in documentation

Maintainability Requirements
-------------------------------------------------------------------------------

**NFR-009: Code Quality**

* Type hints for all public and internal APIs
* Test coverage > 95% for all modules
* Automated testing on multiple Python versions
* Linting with ruff, type checking with pyright

**NFR-010: Architectural Clarity**

* Clear separation between public API and implementation
* Layered architecture documented
* Dependency on stable libraries (classcore, dynadoc)
* Minimal external dependencies

Reliability Requirements
-------------------------------------------------------------------------------

**NFR-011: Robustness**

* Graceful handling of edge cases (empty collections, None values)
* No silent failures or data corruption
* Consistent behavior across Python versions
* Memory safety (no segmentation faults)

Security Requirements
-------------------------------------------------------------------------------

**NFR-012: Practical Immutability**

* Immutability enforced for normal usage patterns
* Clear documentation that circumvention is possible
* Not intended as security boundary
* Protection against accidental modification, not malicious circumvention

Constraints and Assumptions
===============================================================================

Technical Constraints
-------------------------------------------------------------------------------

* Python language limitations make true immutability impossible
* Must allow attribute setting during ``__init__`` for compatibility
* Cannot prevent all circumvention methods (``object.__setattr__``, etc.)
* Delegation to classcore for core immutability mechanisms

Dependency Constraints
-------------------------------------------------------------------------------

* Depends on classcore for class factory and protection mechanisms
* Depends on dynadoc for documentation generation
* Depends on absence for sentinel values
* Depends on typing_extensions for backported type features

Compatibility Constraints
-------------------------------------------------------------------------------

* Must work with dataclasses decorator
* Must support Python's pickling protocol
* Must be compatible with metaclass conflicts resolution
* Must work with standard library introspection tools

Performance Constraints
-------------------------------------------------------------------------------

* Cannot use runtime code generation (impacts startup time)
* Cannot significantly impact import time
* Memory overhead must remain reasonable for large collections
* Attribute access must remain fast for real-time applications

Assumptions
-------------------------------------------------------------------------------

* Users understand Python's object model and attribute access
* Users accept that absolute immutability is impossible in Python
* Development environments support Python 3.10+
* Type checkers are used as optional tools, not requirements
* Users willing to adopt new APIs for immutability benefits

Out of Scope
===============================================================================

The following features are explicitly excluded from frigid's scope:

**Security-Hardened Immutability**

* Frigid does not prevent determined circumvention
* Not suitable as security boundary or sandbox
* Use Python's restricted execution or separate processes for security

**Deep Freezing of Nested Structures**

* Frigid does not recursively freeze nested mutable objects
* Users must explicitly create immutable nested structures
* No automatic conversion of mutable contents to immutable

**Immutable Built-in Collections**

* No immutable list (use tuple)
* No immutable set (use frozenset)
* Frigid focuses on types not provided by Python standard library

**Runtime Performance Optimization**

* No C extensions for performance optimization
* No JIT compilation or bytecode manipulation
* Relies on Python's standard attribute access mechanisms

**Immutability Analysis Tools**

* No static analysis for detecting mutations
* No linting rules for enforcing immutability
* Users should use type checkers for static guarantees

**Automatic Migration Tools**

* No automated refactoring from mutable to immutable code
* No codemod tools for converting existing code
* Users perform manual migration using documentation

**Immutable I/O or External Resources**

* No immutable file handles or network connections
* No immutable database connections
* Scope limited to in-memory data structures

**Thread Synchronization Primitives**

* No locks, semaphores, or other concurrency primitives
* Immutability aids thread safety but does not replace synchronization
* Users must still implement proper concurrent access patterns