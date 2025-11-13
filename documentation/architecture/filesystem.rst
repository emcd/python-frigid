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
Filesystem Organization
*******************************************************************************

This document describes the specific filesystem organization for the project,
showing how the standard organizational patterns are implemented for this
project's configuration. For the underlying principles and rationale behind
these patterns, see the `common architecture documentation
<https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/architecture.rst>`_.

Project Structure
===============================================================================

Root Directory Organization
-------------------------------------------------------------------------------

The project implements the standard filesystem organization:

.. code-block::

    python-frigid/
    ├── LICENSE.txt              # Project license
    ├── README.rst               # Project overview and quick start
    ├── pyproject.toml           # Python packaging and tool configuration
    ├── documentation/           # Sphinx documentation source
    ├── sources/                 # All source code
    ├── tests/                   # Test suites
    └── .auxiliary/              # Development workspace

Source Code Organization
===============================================================================

Package Structure
-------------------------------------------------------------------------------

The main Python package follows the standard ``sources/`` directory pattern:

.. code-block::

    sources/
    └── frigid/                      # Main Python package
        ├── __/                      # Centralized import hub (internal)
        │   ├── __init__.py          # Re-exports core utilities
        │   ├── imports.py           # External library imports
        │   ├── dictionaries.py      # ImmutableDictionary implementation
        │   ├── doctab.py            # Documentation fragments table
        │   ├── exceptions.py        # Internal exception classes
        │   └── nomina.py            # Type aliases and naming utilities
        ├── __init__.py              # Package entry point (public API)
        ├── py.typed                 # Type checking marker for mypy/pyright
        ├── classes.py               # Metaclasses and decorators for immutable classes
        ├── dictionaries.py          # Public immutable dictionary types
        ├── exceptions.py            # Public exception hierarchy
        ├── installers.py            # Utilities for installing into builtins
        ├── modules.py               # Immutable module types
        ├── namespaces.py            # Immutable namespace objects
        └── sequences.py             # Immutable sequence utilities

All package modules use the standard ``__`` import pattern as documented
in the common architecture guide.

Module Purposes
-------------------------------------------------------------------------------

**Public API Modules** (directly under ``sources/frigid/``):

``__init__.py``
  Package entry point that re-exports the public API. Imports and exposes:

  * Core classes (Dictionary, ValidatorDictionary, Namespace, Object, etc.)
  * Metaclasses (Class, Dataclass, AbstractBaseClass, Protocol variants)
  * Decorators (with_standard_behaviors, dataclass_with_standard_behaviors)
  * Exception classes (AttributeImmutability, EntryImmutability, etc.)
  * Utility functions (one, finalize_module)

``classes.py``
  Metaclasses and decorators for creating immutable classes:

  * Metaclasses: Class, Dataclass, DataclassMutable, AbstractBaseClass,
    ProtocolClass, ProtocolDataclass, ProtocolDataclassMutable
  * Base classes: Object, ObjectMutable, DataclassObject,
    DataclassObjectMutable, Protocol variants
  * Decorators: with_standard_behaviors, dataclass_with_standard_behaviors
  * All delegate to classcore.standard.class_factory with frigid configuration

``dictionaries.py``
  Immutable dictionary implementations:

  * AbstractDictionary: Base class defining immutable dictionary interface
  * Dictionary: Standard immutable dictionary (wraps ImmutableDictionary)
  * ValidatorDictionary: Dictionary with validation on initialization
  * Supports set operations (union ``|``, intersection ``&``)

``exceptions.py``
  Public exception hierarchy:

  * Omniexception: Base exception for all frigid exceptions
  * Omnierror: Base error (inherits from Omniexception)
  * AttributeImmutability: Raised when modifying immutable attributes
  * EntryImmutability: Raised when modifying immutable dictionary entries
  * EntryInvalidity: Raised when dictionary validation fails

``installers.py``
  Utilities for installing frigid functions into Python builtins:

  * install_into_builtins(): Adds frigid utilities to builtins module
  * Opt-in mechanism for making frigid functions globally available

``modules.py``
  Immutable module types and utilities:

  * Module: Immutable module class (extends types.ModuleType)
  * finalize_module(): Combines dynadoc generation with module reclassification
  * Prevents modification of module-level constants after finalization

``namespaces.py``
  Immutable namespace objects:

  * Namespace: Similar to types.SimpleNamespace but immutable
  * Initialization from iterables, mappings, and keyword arguments
  * Uses ImmutableDictionary for __dict__ storage

``sequences.py``
  Immutable sequence utilities:

  * one(): Creates single-item tuple more readably than ``(x,)`` syntax
  * Minimal module focused on ergonomic tuple creation

**Internal Implementation** (under ``sources/frigid/__/``):

``__init__.py``
  Re-exports commonly used imports for internal use:

  * All imports from imports.py
  * All type aliases from nomina.py
  * Makes ``from . import __`` work consistently

``imports.py``
  Centralized external library imports:

  * Standard library: abc, collections.abc, dataclasses, functools, types
  * Third-party: classcore, dynadoc, absence, typing_extensions
  * Provides consistent namespace for all frigid modules
  * Reduces import duplication and eases dependency management

``dictionaries.py``
  Core immutable dictionary implementation:

  * ImmutableDictionary: Subclasses dict with immutability enforcement
  * Uses _behaviors_ set to track immutability state
  * Allows modifications during __init__, blocks after initialization
  * Foundation for all dictionary-based immutable structures

``doctab.py``
  Documentation fragments for dynamic documentation:

  * Reusable documentation strings for classes and behaviors
  * Used by dynadoc to generate comprehensive docstrings
  * Organized by topic (classes, modules, behaviors, etc.)

``exceptions.py``
  Internal exception classes:

  * EntryImmutability: Internal version for dictionary operations
  * OperationInvalidity: Raised for invalid operations on immutable collections
  * Used by implementation layer before being re-raised as public exceptions

``nomina.py``
  Type aliases, type variables, and naming utilities:

  * Type variables: H (hashable), V (value), etc.
  * Type aliases for common signatures
  * calculate_attrname(): Generates package-specific attribute names
  * Provides consistent naming across the package

Component Integration
===============================================================================

Import Pattern Implementation
-------------------------------------------------------------------------------

All public modules follow the centralized import pattern:

.. code-block:: python

    # In any public module (e.g., dictionaries.py, namespaces.py)
    from . import __

    # Usage throughout the module
    class Dictionary( __.cabc.Mapping[ __.H, __.V ] ):
        ''' Immutable dictionary implementation. '''
        def __init__( self, *args: __.typx.Any, **kwargs: __.typx.Any ):
            self._data_ = __.ImmutableDictionary( *args, **kwargs )

This pattern provides:

* Consistent access to external dependencies (classcore, dynadoc, absence)
* Type aliases (cabc for collections.abc, typx for typing extensions)
* Internal utilities (ImmutableDictionary, calculate_attrname)
* Reduced per-module import overhead

The ``__`` package acts as a single source of truth for all dependencies,
making it easy to update dependencies or add new ones without modifying
individual modules.

Exception Organization
-------------------------------------------------------------------------------

Package-wide exceptions are centralized in ``sources/frigid/exceptions.py``
following the standard hierarchy patterns documented in the `common practices guide
<https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/practices.rst>`_.

The exception hierarchy follows this structure:

.. code-block::

    Omniexception (base for all frigid exceptions)
    └── Omnierror (base for error conditions)
        ├── AttributeImmutability (attribute modification violations)
        ├── EntryImmutability (dictionary entry modification violations)
        └── EntryInvalidity (validation failures)

Each exception class inherits from both the frigid base and an appropriate
Python built-in exception:

* ``AttributeImmutability`` → ``Omnierror`` + ``AttributeError``
* ``EntryImmutability`` → ``Omnierror`` + ``TypeError``
* ``EntryInvalidity`` → ``Omnierror`` + ``ValueError``

This dual inheritance ensures exceptions are catchable both through frigid's
hierarchy and through standard Python exception types.

Documentation Integration
-------------------------------------------------------------------------------

The package uses dynadoc for dynamic documentation generation:

**Documentation Fragments** (``sources/frigid/__/doctab.py``):

* Centralized table of reusable documentation strings
* Organized by category (classes, modules, behaviors)
* Enables consistent documentation across similar components

**Fragment Usage**:

.. code-block:: python

    class Dictionary:
        _dynadoc_fragments_ = {
            'description': doctab.classes.Dictionary.description,
            'examples': doctab.classes.Dictionary.examples,
        }

**Benefits**:

* Reduces documentation duplication
* Ensures consistency across similar classes
* Facilitates documentation updates
* Supports multiple documentation renderers

Test Organization
===============================================================================

Tests mirror the source package structure and follow project naming conventions.
For detailed information about test structure, naming conventions, and coverage
targets, see ``architecture/testplans/index.rst``.

Documentation Organization
===============================================================================

Documentation Structure
-------------------------------------------------------------------------------

Project documentation resides in ``documentation/``:

.. code-block::

    documentation/
    ├── index.rst                   # Documentation home
    ├── prd.rst                    # Product requirements document
    ├── contribution.rst           # Contribution guidelines
    ├── architecture/               # Architecture documentation
    │   ├── index.rst              # Architecture overview
    │   ├── summary.rst            # System architecture summary
    │   ├── filesystem.rst         # This file
    │   ├── decisions/             # Architectural decision records
    │   ├── designs/               # Detailed design documents
    │   └── testplans/             # Test planning documentation
    └── examples/                   # Usage examples for each module

Documentation Types
-------------------------------------------------------------------------------

**API Documentation**:

* Generated from source code docstrings
* Uses Sphinx with autodoc extension
* Includes type hints and examples
* Available at package documentation site

**Architecture Documentation**:

* High-level system design
* Component relationships
* Architectural decision records
* Design patterns and rationale

**Examples Documentation**:

* Practical usage examples
* Common patterns and idioms
* Migration guides
* Tested via doctest

**Requirements Documentation**:

* Product requirements (prd.rst)
* Feature specifications
* Success criteria
* Constraints and assumptions

Development Workspace
===============================================================================

Development-specific files are organized in ``.auxiliary/``:

.. code-block::

    .auxiliary/
    ├── notes/                       # Development notes and session state
    ├── scribbles/                   # Temporary scratch files
    └── instructions/                # Cached development guidelines

Purpose and Usage
-------------------------------------------------------------------------------

**Session Continuity**:

* ``.auxiliary/notes/`` preserves development context across sessions
* Claude Code agents update notes during conversations
* TODO items track remaining work and emergent tasks
* Session notes capture decisions and context

**Development Resources**:

* ``.auxiliary/instructions/`` caches commonly-referenced guidelines
* Populated by agentsmgr tool from upstream repositories
* Provides offline access to development standards
* Ensures consistency with project templates

**Scratch Space**:

* ``.auxiliary/scribbles/`` for temporary experiments
* Preferred over ``/tmp/`` for project-specific scratch work
* Not committed to version control
* Cleaned up periodically

Exclusion from Distribution
-------------------------------------------------------------------------------

The ``.auxiliary/`` directory is excluded from package distributions:

* Listed in ``.gitignore`` for local development files
* Excluded via ``tool.hatch.build`` configuration in ``pyproject.toml``
* Not included in source distributions
* Development-specific only, not needed by users

Configuration Files
===============================================================================

``pyproject.toml``
  Centralized project configuration following PEP 518/PEP 621 with package
  metadata, dependencies, build system (hatch), and tool configurations
  (pytest, coverage, ruff, pyright).

``README.rst``
  Project overview with key features, installation instructions, basic
  examples, and contribution guidelines.

``LICENSE.txt``
  Apache License 2.0 with copyright and legal terms.

Architecture Evolution
===============================================================================

This filesystem organization provides a foundation that architect agents can
evolve as the project grows. For questions about organizational principles,
subpackage patterns, or testing strategies, refer to the comprehensive common
documentation:

* `Architecture Patterns <https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/architecture.rst>`_
* `Development Practices <https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/practices.rst>`_
* `Test Development Guidelines <https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/tests.rst>`_
