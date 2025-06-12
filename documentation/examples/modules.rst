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


Modules
===============================================================================

Module Objects
-------------------------------------------------------------------------------

Immutable modules prevent any modification of attributes after creation. This
makes them useful for ensuring that module-level constants remain constant and
that module interfaces remain stable during runtime.

.. doctest:: Modules

    >>> from frigid import Module

Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While modules are typically initialized during import of their sources, they
may also be created dynamically. As with standard Python modules, a name is
required when dynamically creating a module.

.. doctest:: Modules

    >>> constants = Module( 'constants' )
    >>> constants
    <module 'constants'>

Immutability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once created, a module becomes completely immutable. Even built-in attributes
cannot be modified:

.. doctest:: Modules

    >>> constants.__name__ = 'renamed'
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutability: Could not assign or delete attribute '__name__' on instance of class ...

Attributes cannot be deleted:

.. doctest:: Modules

    >>> del constants.__name__
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutability: Could not assign or delete attribute '__name__' on instance of class ...

And new attributes cannot be added:

.. doctest:: Modules

    >>> constants.PI = 3.14159
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutability: Could not assign or delete attribute 'PI' on instance of class ...

Mass Reclassification
-------------------------------------------------------------------------------

For cases where multiple modules need to be protected, the
``reclassify_modules`` function can convert all modules in a package to
immutable modules. This is particularly useful in package ``__init__.py`` files
to protect all submodules:

.. code-block:: python

    from frigid import reclassify_modules
    reclassify_modules( __name__ )

.. warning::

    While immutable modules prevent direct attribute modification, they cannot
    prevent all forms of tampering. In particular, direct manipulation of a
    module's ``__dict__`` is still possible. Use immutable modules to prevent
    accidental modifications and basic tampering attempts, but do not rely on
    them for security-critical protections.
