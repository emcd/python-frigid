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

Immutable objects do not allow instance attributes to be assigned, reassigned,
or deleted after instantiation. Immutable objects can be created via decoration
(by ``@immutable``) or inheritance (from ``Object``).

.. doctest:: Objects

    >>> from frigid import Object, immutable

Decorator
-------------------------------------------------------------------------------

The ``@immutable`` decorator can be applied to existing classes to make their
instances immutable after initialization:

.. doctest:: Objects

    >>> @immutable
    ... class Temperature:
    ...     def __init__( self, kelvin ):
    ...         if kelvin < 0:
    ...             raise ValueError( "Temperature cannot be below absolute zero" )
    ...         self.kelvin = kelvin
    ...         self.celsius = kelvin - 273.15
    ...         self.fahrenheit = self.celsius * 9/5 + 32

The class works normally during initialization:

.. doctest:: Objects

    >>> water_boiling = Temperature( 373.15 )
    >>> water_boiling.celsius
    100.0

But becomes immutable afterwards:

.. doctest:: Objects

    >>> water_boiling.kelvin = 0  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'kelvin'.

The decorator preserves the validation logic in the class:

.. doctest:: Objects

    >>> impossible = Temperature( -1 )  # Attempt invalid initialization
    Traceback (most recent call last):
    ...
    ValueError: Temperature cannot be below absolute zero


Mutable Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``mutables`` argument can allow some attributes to remain mutable after
assignment.

.. doctest:: Objects

    >>> @immutable( mutables = ( 'version', ) )
    ... class VersionedConfig:
    ...     def __init__( self, name, version ):
    ...         self.name = name
    ...         self.version = version
    ...
    >>> config = VersionedConfig( 'MyApp', '1.0.0' )

Reassignment of mutable attribute:

.. doctest:: Objects

    >>> config.version = '1.0.1'  # This works fine
    >>> config.version
    '1.0.1'

Deletion of mutable attribute:

.. doctest:: Objects

    >>> del config.version  # This works with mutable attributes
    >>> hasattr( config, 'version' )
    False


Docstrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``docstring`` argument can set or override the docstring of the decorated
class. This is useful when docstrings need to be computed dynamically:

.. doctest:: Objects

    >>> @immutable( docstring = 'A configuration class with custom documentation.' )
    ... class DocumentedConfig:
    ...     '''Original docstring that will be replaced.'''
    ...     def __init__( self, name ):
    ...         self.name = name
    ...
    >>> print( DocumentedConfig.__doc__ )
    A configuration class with custom documentation.


Slotted Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``@immutable`` decorator works with classes which use ``__slots__`` for
attribute storage. Remember to include the ``_behaviors_`` slot:

.. doctest:: Objects

    >>> @immutable
    ... class Vector:
    ...     __slots__ = ( 'x', 'y', 'z', '_behaviors_' )
    ...
    ...     def __init__( self, x, y, z ):
    ...         self.x = x
    ...         self.y = y
    ...         self.z = z
    ...
    >>> v = Vector( 1, 2, 3 )
    >>> v.x = 0  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.


Base Class
-------------------------------------------------------------------------------

The ``Object`` class serves as a base for creating immutable objects.
Attributes must be set in the ``__init__`` method of the derived class before
calling ``super( ).__init__( )``, after which the object becomes immutable.

Here's an example of a point class with immutable coordinates:

.. doctest:: Objects

    >>> class Point( Object ):
    ...     def __init__( self, x, y ):
    ...         self.x = x
    ...         self.y = y
    ...         super( ).__init__( )

The object behaves normally during initialization:

.. doctest:: Objects

    >>> point = Point( 3, 4 )
    >>> point.x
    3

After initialization, attributes cannot be modified:

.. doctest:: Objects

    >>> point.x = 5
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.

Nor can they cannot be deleted:

.. doctest:: Objects

    >>> del point.y
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'y'.

And new attributes cannot be added:

.. doctest:: Objects

    >>> point.z = 0
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'z'.

.. warning::

    When working with built-in types, such as exception types, in multiple
    inheritance hierarchies, avoid using the ``Object`` base class which uses
    ``__slots__``. Instead, apply the ``@accretive`` decorator directly to your
    class.


Multiple Inheritance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using the ``Object`` class with multiple inheritance, be aware of
potential layout conflicts with built-in types that have their own memory
layout:

.. doctest:: Objects

    >>> # This would raise a TypeError due to memory layout conflict
    >>> # class InvalidCombination( BaseException, Object ):
    >>> #     pass

Instead, use the ``@immutable`` decorator directly:

.. doctest:: Objects

    >>> @immutable
    ... class ValidException( BaseException ):
    ...     ''' An exception with immutable behavior. '''
    ...     pass
    ...
    >>> ex = ValidException( 'Something went wrong' )
    >>> ex.context = 'Additional information'
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'context'.
