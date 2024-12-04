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


Aliases
===============================================================================

The ``frigid.qaliases`` module provides qualified aliases for immutable data
structures. These aliases are prefixed with "Immutable" to clearly indicate
their behavior and avoid namespace conflicts.

.. doctest:: QualifiedAliases

    >>> from frigid.qaliases import ImmutableDictionary, ImmutableNamespace
    >>> from frigid import Dictionary, Namespace

The qualified aliases are equivalent to their original classes:

.. doctest:: QualifiedAliases

    >>> ImmutableDictionary is Dictionary
    True
    >>> ImmutableNamespace is Namespace
    True

This is particularly useful when working in codebases that might have multiple
dictionary or namespace implementations:

.. doctest:: QualifiedAliases

    >>> from types import SimpleNamespace
    >>> from collections import UserDict
    >>>
    >>> # Clear which one is immutable
    >>> config = ImmutableNamespace( debug = True )
    >>> data = ImmutableDictionary( count = 42 )

All core classes have qualified aliases:

.. doctest:: QualifiedAliases

    >>> from frigid.qaliases import (
    ...     # Class factories
    ...     ImmutableClass,
    ...     ImmutableABCFactory,
    ...     ImmutableProtocolClass,
    ...     # Dictionaries
    ...     AbstractImmutableDictionary,
    ...     ImmutableDictionary,
    ...     ImmutableValidatorDictionary,
    ...     # Other types
    ...     ImmutableModule,
    ...     ImmutableNamespace,
    ...     ImmutableObject,
    ... )
