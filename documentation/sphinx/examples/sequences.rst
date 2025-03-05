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


Sequences
===============================================================================


``one`` Function (Single-Element Tuples)
-------------------------------------------------------------------------------

The ``one`` function provides a cleaner alternative to Python's comma-syntax
for creating single-item tuples. It can be used directly from the package or
installed into builtins.

Basic Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Import and use directly from the package:

.. doctest:: Sequences

    >>> from frigid import one
    >>> single42 = one( 42 )
    >>> single42
    (42,)

This is equivalent to the standard comma-syntax but more readable in many
contexts:

.. doctest:: Sequences

    >>> one( 42 ) == ( 42, )
    True

Common Use Cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating lists of single-item tuples is clearer with ``one``:

.. doctest:: Sequences

    >>> numbers = [ one( x ) for x in range( 3 ) ]
    >>> numbers
    [(0,), (1,), (2,)]

It works well with ``map`` and other higher-order functions:

.. doctest:: Sequences

    >>> tuple( map( one, [ 'a', 'b', 'c' ] ) )
    (('a',), ('b',), ('c',))

Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function can be installed into builtins for easier access:

.. doctest:: Sequences

    >>> from frigid import install
    >>> install( )  # Installs as 'one'
    >>> one( 'test' )   # Now available globally
    ('test',)
    >>> install( 'single' )  # Install with custom name
    >>> single( 'test' )
    ('test',)
