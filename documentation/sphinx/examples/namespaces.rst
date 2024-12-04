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


Namespace
===============================================================================

Immutable namespaces are similar to :py:class:`types.SimpleNamespace`, but
prevent any modification of attributes after creation. This makes them ideal for
configuration objects, settings, or any data structure that should remain
completely unchanged after initialization.

.. doctest:: Namespace

    >>> from frigid import Namespace

Let's illustrate this with a configuration namespace for a database connection:

.. doctest:: Namespace

    >>> db_config = Namespace(
    ...     host = 'localhost',
    ...     port = 5432,
    ...     name = 'myapp',
    ...     user = 'admin',
    ...     password = 'secret',
    ...     pool_size = 10,
    ...     ssl = True,
    ... )

Initialization
-------------------------------------------------------------------------------

Immutable namespaces can be initialized from zero or more dictionaries or
iterables over key-value pairs and zero or more keyword arguments.

.. doctest:: Namespace

    >>> # From key-value pairs
    >>> cache = Namespace(
    ...     [ ( 'backend', 'redis' ), ( 'timeout', 300 ) ],
    ... )
    >>> # From dictionary
    >>> logging = Namespace(
    ...     { 'level': 'INFO', 'format': '%(levelname)s: %(message)s' },
    ... )
    >>> # Mixed initialization
    >>> server = Namespace(
    ...     { 'host': 'example.com' },
    ...     [ ( 'port', 443 ) ],
    ...     ssl = True,
    ...     workers = 4,
    ... )

Immutability
-------------------------------------------------------------------------------

Once created, a namespace becomes completely immutable. Attempts to modify
existing attributes will raise an error:

.. doctest:: Namespace

    >>> db_config.port = 3306
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'port'.

Attempts to delete attributes are also prevented:

.. doctest:: Namespace

    >>> del db_config.password
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'password'.

Unlike :py:class:`types.SimpleNamespace`, new attributes cannot be added after
creation:

.. doctest:: Namespace

    >>> db_config.timeout = 30
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'timeout'.

Attribute Access
-------------------------------------------------------------------------------

Attributes can be accessed normally through dot notation:

.. doctest:: Namespace

    >>> db_config.host
    'localhost'
    >>> db_config.port
    5432

Attempting to access non-existent attributes raises an AttributeError:

.. doctest:: Namespace

    >>> db_config.missing
    Traceback (most recent call last):
    ...
    AttributeError: 'Namespace' object has no attribute 'missing'

Representation
-------------------------------------------------------------------------------

Namespaces have a clear string representation that shows all their attributes:

.. doctest:: Namespace

    >>> cache
    frigid.namespaces.Namespace( backend = 'redis', timeout = 300 )
    >>> logging
    frigid.namespaces.Namespace( level = 'INFO', format = '%(levelname)s: %(message)s' )

Empty namespaces are also represented appropriately:

.. doctest:: Namespace

    >>> empty = Namespace()
    >>> empty
    frigid.namespaces.Namespace( )

Comparison
-------------------------------------------------------------------------------

Namespaces can be compared with other namespaces or SimpleNamespaces. Two
namespaces are considered equal if they have the same attributes with the same
values:

.. doctest:: Namespace

    >>> from types import SimpleNamespace
    >>> ns1 = Namespace( x = 1, y = 2 )
    >>> ns2 = Namespace( x = 1, y = 2 )
    >>> ns3 = SimpleNamespace( x = 1, y = 2 )
    >>> ns1 == ns2  # Same type, same content
    True
    >>> ns1 == ns3  # Different type, same content
    True
    >>> ns1 == Namespace( x = 1, z = 3 )  # Different content
    False

Copying
-------------------------------------------------------------------------------

To create a copy of a namespace, access its underlying ``__dict__`` and use it
to initialize a new namespace:

.. doctest:: Namespace

    >>> original = Namespace( x = 1, y = 2 )
    >>> copy = Namespace( **original.__dict__ )  #**
    >>> original == copy
    True

This pattern is particularly useful when you need to create a modified version
of an existing configuration:

.. doctest:: Namespace

    >>> # Create new dict with overridden values
    >>> test_config = dict( db_config.__dict__ )
    >>> test_config.update( name = 'test_myapp', host = 'test.localhost' )
    >>> test_db = Namespace( **test_config )  #**
    >>> test_db.name
    'test_myapp'
    >>> test_db.port  # Preserved from original
    5432
