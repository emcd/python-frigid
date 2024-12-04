

.. towncrier release notes start

Frigid 1.0 (2024-12-04)
=======================

Features
--------

- Add ``Dictionary`` class providing completely immutable dictionaries that
  prevent any modification after creation.  Supports standard dictionary
  operations like key lookup, iteration, and views.

- Add ``ValidatorDictionary`` class that validates entries during creation
  using a supplied predicate function.  The validator receives both key and
  value and must return a boolean indicating validity.

- Add set operations for dictionaries:

  * Union operation (``|``) combines two dictionaries while preventing key
    conflicts
  * Intersection operation (``&``) creates new dictionaries either by matching
    key-value pairs with another mapping or by filtering keys with a set

- Add ``Namespace`` class providing a completely immutable alternative to
  ``types.SimpleNamespace``.  All attributes must be set during initialization
  and cannot be modified afterward.

- Add ``Module`` class and ``reclassify_modules`` function for creating and
  converting to immutable modules.  This prevents runtime modification of
  module attributes, helping ensure interface stability.

- Add ``Object`` base class for creating objects with immutable attributes.
  Derived classes must set attributes in ``__init__`` before calling
  ``super().__init__()``.

- Add ``@immutable`` decorator for making existing classes immutable after
  initialization.  Compatible with most classes except those defining their own
  ``__setattr__`` or ``__delattr__`` methods.

- Add metaclasses for creating classes with immutable class attributes:

  * ``Class`` for standard classes
  * ``ABCFactory`` for abstract base classes
  * ``ProtocolClass`` for protocol classes

- Add qualified aliases in ``qaliases`` module with "Immutable" prefix for all
  core classes, helping avoid namespace conflicts.

- Add comprehensive type annotations and ``py.typed`` file for static type
  checking support.

Supported Platforms
-------------------

- Add support for CPython 3.10 to 3.13.
- Add support for PyPy 3.10.
