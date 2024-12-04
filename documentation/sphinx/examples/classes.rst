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


Standard Classes
===============================================================================

Immutable classes are similar to standard Python classes, but prevent any
modification of class attributes after creation. This makes them ideal for
defining constants, enumerations, or configurations that should be completely
immutable.

.. doctest:: Class

    >>> from frigid import Class

Basic Usage
-------------------------------------------------------------------------------

Immutable classes can be defined using the ``Class`` metaclass. Attributes must
be defined during class creation.

.. doctest:: Class

    >>> class Constants( metaclass = Class ):
    ...     PI = 3.14159
    ...     E = 2.71828
    ...     PHI = 1.61803

Once defined, these attributes are protected from any modification:

.. doctest:: Class

    >>> Constants.PI = 3.14  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'PI'.

They cannot be deleted:

.. doctest:: Class

    >>> del Constants.E  # Attempt to delete
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'E'.

And new attributes cannot be added after class creation:

.. doctest:: Class

    >>> Constants.SQRT2 = 1.4142  # Attempt to add
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'SQRT2'.

Decorator Support
-------------------------------------------------------------------------------

Classes can be modified during creation using decorators. This allows for
programmatic addition of attributes before the class becomes immutable.

.. doctest:: Class

    >>> def add_computed_constants( cls ):
    ...     cls.TAU = cls.PI * 2
    ...     return cls
    ...
    >>> class CircleConstants( metaclass = Class, decorators = ( add_computed_constants, ) ):
    ...     PI = 3.14159

The decorator-added attributes become part of the immutable class:

.. doctest:: Class

    >>> CircleConstants.TAU
    6.28318
    >>> CircleConstants.TAU = 6.28  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'TAU'.

Dynamic Docstrings
-------------------------------------------------------------------------------

Classes can be given docstrings dynamically at creation time, which can be
useful for generating documentation programmatically:

.. doctest:: Class

    >>> docstring = 'Configuration for database connection.'
    >>> class DBConfig( metaclass = Class, docstring = docstring ):
    ...     ''' This docstring will be replaced. '''
    ...     HOST = 'localhost'
    ...     PORT = 5432
    >>> DBConfig.__doc__ == docstring
    True

Abstract Base Classes
===============================================================================

The ``ABCFactory`` metaclass creates immutable abstract base classes. This is
particularly useful for defining stable interfaces that should not change after
definition.

.. doctest:: ABCFactory

    >>> from frigid import ABCFactory
    >>> from abc import abstractmethod

    >>> class DataStore( metaclass = ABCFactory ):
    ...     @abstractmethod
    ...     def get( self, key ): pass
    ...
    ...     @abstractmethod
    ...     def put( self, key, value ): pass
    ...
    ...     ENCODING = 'utf-8'

The abstract methods and class attributes are protected:

.. doctest:: ABCFactory

    >>> # Cannot modify abstract interface
    >>> def new_method( self ): pass
    >>> DataStore.list_keys = new_method
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'list_keys'.
    >>> # Cannot modify class attributes
    >>> DataStore.ENCODING = 'ascii'
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'ENCODING'.

Protocol Classes
===============================================================================

The ``ProtocolClass`` metaclass creates immutable protocol classes, which is
useful for defining static type interfaces.

.. doctest:: ProtocolClass

    >>> from frigid import ProtocolClass
    >>> from typing import Protocol

    >>> class Comparable( Protocol, metaclass = ProtocolClass ):
    ...     def __lt__( self, other ) -> bool: ...
    ...     def __gt__( self, other ) -> bool: ...
    ...
    ...     ORDERING = 'natural'

The protocol interface is protected from modification:

.. doctest:: ProtocolClass

    >>> # Cannot modify protocol interface
    >>> def eq( self, other ) -> bool: ...
    >>> Comparable.__eq__ = eq
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute '__eq__'.
    >>> # Cannot modify class attributes
    >>> Comparable.ORDERING = 'reverse'
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'ORDERING'.
