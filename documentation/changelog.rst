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
Release Notes
*******************************************************************************

.. towncrier release notes start

Frigid 4.0 (2025-06-14)
=======================

Enhancements
------------

- Add concealment of non-public attributes to standard behaviors of classes and
  objects.
- Documentation: Add comprehensive examples for classes and update all examples
  for the new architecture.


Removals
--------

- Exceptions: Rename exception classes for better consistency.

  * ``AttributeImmutabilityError`` is now ``AttributeImmutability``
  * ``EntryImmutabilityError`` is now ``EntryImmutability``
  * ``EntryValidityError`` is now ``EntryInvalidity``

  This is a breaking change - the old exception names are no longer available.
- Merge ``dataclasses`` and ``objects`` modules into ``classes`` module.
  Remove ``qaliases`` module.
- Replace ``@immutable`` decorator with ``@with_standard_behaviors``.
  Replace ``@immutable_dataclass`` decorator with
  ``@dataclass_with_standard_behaviors``.


Frigid 3.0 (2025-03-04)
=======================

Documentation Improvements
--------------------------

- Improve organization of examples. Improve wording in various places.


Features
--------

- Add metaclasses for immutable dataclasses including ``Dataclass``,
  ``CompleteDataclass``, ``ProtocolDataclass``, and
  ``CompleteProtocolDataclass``. These factory classes combine Python's dataclass
  functionality with immutable behavior for type-safe, attribute-stable data
  containers.
- Enhance the ``immutable`` decorator to accept optional parameters including
  ``docstring`` for setting or overriding class documentation and ``mutables``
  for specifying attributes that should remain modifiable after initial
  assignment.


Frigid 2.0 (2025-01-23)
=======================

Features
--------

- Add ``one`` function which produces 1-element tuples. Cleaner to read than the
  1-element tuple syntax and is useful for some functional programming contexts.
  Also, add ``install`` function to install ``one`` as a Python, if desired.
- Support ``mutables`` argument when using metaclasses from ``frigid.classes``.
  Allows for selective mutability of class attributes.
- ⚠️  BREAKING CHANGES! ⚠️  Improve ``reclassify_modules`` to constrain
  reclassification to only package modules and not other modules outside of
  package. Alter interface to make recursion through subpackages optional. Accept
  module objects and module names in addition to module attributes dictionaries.
  Attributes dictionaries must contain ``__package__`` or ``__name__`` attribute
  now.


Frigid 1.0 (2024-12-04)
=======================

Features
--------

- Add ``@immutable`` decorator for making instances of existing classes immutable
  after initialization. Compatible with most classes except those defining their
  own ``__setattr__`` or ``__delattr__`` methods.
- Add ``Module`` class and ``reclassify_modules`` function for creating and
  converting to immutable modules. This prevents runtime modification of module
  attributes, helping ensure interface stability.
- Add ``Namespace`` class providing a completely immutable alternative to
  ``types.SimpleNamespace``. All attributes must be set during initialization
  and cannot be modified afterward.
- Add ``Object`` base class for creating objects with immutable attributes.
  Derived classes must set attributes in ``__init__`` before calling
  ``super().__init__()``.
- Add immutable dictionaries, which have additional methods, such as ``copy`` and
  ``with_data``, additional operations, such as union (``|``) and intersection
  (``&``):

    * ``Dictionary`` for simple immutable mappings
    * ``ValidatorDictionary`` which uses a provided validator function
- Add metaclasses for creating classes with immutable class attributes:

    * ``Class`` for standard classes
    * ``ABCFactory`` for abstract base classes
    * ``ProtocolClass`` for protocol classes
- Add qualified aliases in ``qaliases`` module with "Immutable" prefix for all
  core classes, helping avoid namespace conflicts.


Supported Platforms
-------------------

- Add support for CPython 3.10 to 3.13.
- Add support for PyPy 3.10.
