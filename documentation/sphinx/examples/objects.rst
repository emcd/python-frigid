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


Objects
===============================================================================

The ``frigid.objects`` module provides tools for creating objects with
immutable attributes. This includes both a base class and a decorator that can
be applied to existing classes.

Base Class
-------------------------------------------------------------------------------

The ``Object`` class serves as a base for creating immutable objects.
Attributes must be set in the derived class's ``__init__`` method before
calling ``super().__init__()``, after which the object becomes immutable.

.. doctest:: Object

    >>> from frigid import Object

Here's an example of a point class with immutable coordinates:

.. doctest:: Object

    >>> class Point( Object ):
    ...     def __init__( self, x, y ):
    ...         self.x = x
    ...         self.y = y
    ...         super( ).__init__( )

The object behaves normally during initialization:

.. doctest:: Object

    >>> point = Point( 3, 4 )
    >>> point.x
    3

After initialization, attributes cannot be modified:

.. doctest:: Object

    >>> point.x = 5
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.

They cannot be deleted:

.. doctest:: Object

    >>> del point.y
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'y'.

And new attributes cannot be added:

.. doctest:: Object

    >>> point.z = 0
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'z'.

Immutable Decorator
-------------------------------------------------------------------------------

The ``@immutable`` decorator can be applied to existing classes to make their
instances immutable after initialization. This is particularly useful for
classes that need to be immutable but have specific initialization
requirements.

.. doctest:: Immutable

    >>> from frigid import immutable

Here's an example of a temperature class that validates its value during
initialization:

.. doctest:: Immutable

    >>> @immutable
    ... class Temperature:
    ...     def __init__( self, kelvin ):
    ...         if kelvin < 0:
    ...             raise ValueError( "Temperature cannot be below absolute zero" )
    ...         self.kelvin = kelvin
    ...         self.celsius = kelvin - 273.15
    ...         self.fahrenheit = self.celsius * 9/5 + 32

The class works normally during initialization:

.. doctest:: Immutable

    >>> water_boiling = Temperature( 373.15 )
    >>> water_boiling.celsius
    100.0

But becomes immutable afterwards:

.. doctest:: Immutable

    >>> water_boiling.kelvin = 0  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'kelvin'.

The decorator preserves the class's validation logic:

.. doctest:: Immutable

    >>> impossible = Temperature( -1 )  # Attempt invalid initialization
    Traceback (most recent call last):
    ...
    ValueError: Temperature cannot be below absolute zero

Decorator Compatibility
-------------------------------------------------------------------------------

The ``@immutable`` decorator cannot be applied to classes that define their own
``__setattr__`` or ``__delattr__`` methods, as this would conflict with the
immutability enforcement:

.. doctest:: Immutable

    >>> @immutable  # This will fail
    ... class Mutable:
    ...     def __setattr__( self, name, value ):
    ...         # Custom attribute setting logic
    ...         super().__setattr__( name, value )
    Traceback (most recent call last):
    ...
    frigid.exceptions.DecoratorCompatibilityError: Cannot decorate class 'Mutable' which defines '__setattr__'.

Slots Support
-------------------------------------------------------------------------------

The ``@immutable`` decorator works with classes that use ``__slots__`` for
attribute storage. Remember to include the ``_behaviors_`` slot:

.. doctest:: Immutable

    >>> @immutable
    ... class Vector:
    ...     __slots__ = ( 'x', 'y', 'z', '_behaviors_' )
    ...
    ...     def __init__( self, x, y, z ):
    ...         self.x = x
    ...         self.y = y
    ...         self.z = z

The slots-based class behaves the same as one using ``__dict__``:

.. doctest:: Immutable

    >>> v = Vector( 1, 2, 3 )
    >>> v.x = 0  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.
