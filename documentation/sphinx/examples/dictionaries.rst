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


Dictionaries
===============================================================================


Simple Dictionary
-------------------------------------------------------------------------------

Simple immutable dictionaries have an interface similar to :py:class:`dict`,
but prevent any modifications after creation. They are useful for configuration
objects, constants, and other scenarios where data should never change after
initialization.

.. doctest:: Dictionary

    >>> from frigid import Dictionary

Let us illustrate this with a configuration dictionary for a hypothetical
application:

.. doctest:: Dictionary

    >>> config = Dictionary(
    ...     database = Dictionary(
    ...         host = 'localhost',
    ...         port = 5432,
    ...         name = 'myapp',
    ...     ),
    ...     cache = Dictionary(
    ...         enabled = True,
    ...         ttl = 3600,
    ...     ),
    ...     debug = False,
    ... )

Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Immutable dictionaries can be initialized from zero or more other dictionaries
or iterables over key-value pairs and zero or more keyword arguments.

.. doctest:: Dictionary

    >>> # From dictionary
    >>> d1 = Dictionary( { 'x': 1, 'y': 2 } )
    >>> # From key-value pairs
    >>> d2 = Dictionary( [ ( 'a', 1 ), ( 'b', 2 ) ] )
    >>> # From keywords
    >>> d3 = Dictionary( foo = 'bar', baz = 42 )
    >>> # Mixed initialization
    >>> d4 = Dictionary( { 'x': 1 }, [ ( 'y', 2 ) ], z = 3 )

Immutability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once created, a namespace becomes completely immutable. Attempts to modify
existing attributes will raise an error:

.. doctest:: Dictionary

    >>> config['debug'] = True  # Attempt to modify
    Traceback (most recent call last):
    ...
    frigid.exceptions.EntryImmutabilityError: Cannot assign entry for 'debug'.

Attempts to delete attributes are also prevented:

.. doctest:: Dictionary

    >>> del config['cache']  # Attempt to delete
    Traceback (most recent call last):
    ...
    frigid.exceptions.EntryImmutabilityError: Cannot assign entry for 'cache'.

Copies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copies can be made which preserve behavior and data.

.. doctest:: Dictionary

    >>> original = Dictionary( x = 1, y = 2 )
    >>> copy = original.copy( )
    >>> copy
    frigid.dictionaries.Dictionary( {'x': 1, 'y': 2} )

Copies can also be made which preserve behavior but replace data. These are
made using the ``with_data`` method, which creates a new dictionary of the same
type but with different data. This is particularly useful with validator
dictionaries (see below) as it preserves their behavior:

.. doctest:: Dictionary

    >>> new = original.with_data( a = 3, b = 4 )
    >>> new
    frigid.dictionaries.Dictionary( {'a': 3, 'b': 4} )

Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The copies are equivalent to their originals.

.. doctest:: Dictionary

    >>> original == copy
    True

And to instances of other registered subclasses of
:py:class:`collections.abc.Mapping` which have equivalent data.

.. doctest:: Dictionary

    >>> original == { 'x': 1, 'y': 2 }
    True

Access of Absent Entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like :py:class:`dict`, the ``get`` method allows for "soft" accesses which
provide a default value if an entry is missing.

.. doctest:: Dictionary

    >>> d = Dictionary( x = 1, y = 2, z = 3 )
    >>> d.get( 'x' )
    1
    >>> d.get( 'missing' )  # Returns None for missing keys
    >>> d.get( 'missing', 'default' )  # Custom default value
    'default'

Views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard dictionary views are available:

.. doctest:: Dictionary

    >>> list( d.keys( ) )
    ['x', 'y', 'z']
    >>> list( d.values( ) )
    [1, 2, 3]
    >>> list( d.items( ) )
    [('x', 1), ('y', 2), ('z', 3)]

Unions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The union operator (``|``) combines entries from two dictionaries or a
dictionary and a mapping, creating a new dictionary. The operation prevents
duplicate keys:

.. doctest:: Dictionary

    >>> auth = Dictionary( user = 'admin', password = 'secret' )
    >>> extra = Dictionary( password = 'newpass', token = 'abc123' )
    >>> # Union creates new dictionary with combined entries
    >>> combined = auth | Dictionary( token = 'xyz789' )
    >>> combined
    frigid.dictionaries.Dictionary( {'user': 'admin', 'password': 'secret', 'token': 'xyz789'} )

When operands have overlapping keys, an error is raised:

.. doctest:: Dictionary

    >>> auth | extra
    Traceback (most recent call last):
    ...
    frigid.exceptions.EntryImmutabilityError: Cannot assign entry for 'password'.

Intersections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The intersection operator (``&``) can be used in two ways:

1. With another mapping to keep entries with matching key-value pairs:

.. doctest:: Dictionary

    >>> d1 = Dictionary( a = 1, b = 2, c = 3 )
    >>> d2 = { 'a': 1, 'b': 5, 'd': 4 }
    >>> d1 & d2  # Only entries matching in both key and value
    frigid.dictionaries.Dictionary( {'a': 1} )

2. With a set or keys view to filter entries by keys:

.. doctest:: Dictionary

    >>> sorted( ( d1 & { 'a', 'c' } ).items( ) )  # Only entries with matching keys
    [('a', 1), ('c', 3)]


Validator Dictionary
-------------------------------------------------------------------------------

Validator dictionaries ensure that all entries satisfy specified criteria at
creation time. The first argument must be a callable which accepts a key and
value and returns a boolean indicating whether the entry is valid.

.. doctest:: ValidatorDictionary

    >>> from frigid import ValidatorDictionary

Here's an example of a dictionary that only accepts string keys and integer
values:

.. doctest:: ValidatorDictionary

    >>> def validate_int_values( key, value ):
    ...     return isinstance( key, str ) and isinstance( value, int )
    ...
    >>> numbers = ValidatorDictionary(
    ...     validate_int_values,
    ...     count = 42,
    ...     items = 10,
    ... )
    >>> numbers
    frigid.dictionaries.ValidatorDictionary( <function validate_int_values at 0x...>, {'count': 42, 'items': 10} )

Invalid entries are rejected during creation:

.. doctest:: ValidatorDictionary

    >>> # Invalid value type
    >>> ValidatorDictionary( validate_int_values, count = '42' )
    Traceback (most recent call last):
    ...
    frigid.exceptions.EntryValidityError: Cannot add invalid entry with key, 'count', and value, '42', to dictionary.
    >>> # Invalid key type
    >>> ValidatorDictionary( validate_int_values, { 42: 42 } )
    Traceback (most recent call last):
    ...
    frigid.exceptions.EntryValidityError: Cannot add invalid entry with key, 42, and value, 42, to dictionary.

When copying validator dictionaries, both ``copy`` and ``with_data`` preserve
the validator:

.. doctest:: ValidatorDictionary

    >>> # Both copies maintain validation
    >>> copy = numbers.copy( )
    >>> new = numbers.with_data( total = 100 )
    >>> # Invalid data still rejected
    >>> numbers.with_data( total = '100' )
    Traceback (most recent call last):
    ...
    frigid.exceptions.EntryValidityError: Cannot add invalid entry with key, 'total', and value, '100', to dictionary.
