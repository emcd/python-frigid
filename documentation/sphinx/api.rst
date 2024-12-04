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

:tocdepth: 4


*******************************************************************************
API
*******************************************************************************


Package ``frigid``
===============================================================================

Data structures which are completely immutable after creation. This behavior is
useful for configuration objects, value objects, and other scenarios requiring
collections with strong immutability guarantees.

* ``Dictionary``: A dict-like structure that becomes completely immutable after
  creation. Includes a ``ValidatorDictionary`` variant, which validates entries
  during creation.

* ``Namespace``: Similar to :py:class:`types.SimpleNamespace` but completely
  immutable after creation.

* ``Module``: A module type that enforces complete attribute immutability.

* ``Object``: Base class for objects with immutable attributes.

* ``Class``: Metaclass for creating classes with immutable class attributes.

* ``immutable``: Decorator for making classes produce immutable instances.


Module ``frigid.dictionaries``
-------------------------------------------------------------------------------

.. automodule:: frigid.dictionaries


Module ``frigid.namespaces``
-------------------------------------------------------------------------------

.. automodule:: frigid.namespaces


Module ``frigid.modules``
-------------------------------------------------------------------------------

.. automodule:: frigid.modules


Module ``frigid.classes``
-------------------------------------------------------------------------------

.. automodule:: frigid.classes


Module ``frigid.objects``
-------------------------------------------------------------------------------

.. automodule:: frigid.objects


Module ``frigid.exceptions``
-------------------------------------------------------------------------------

.. automodule:: frigid.exceptions


Module ``frigid.qaliases``
-------------------------------------------------------------------------------

.. automodule:: frigid.qaliases
   :imported-members:
   :noindex:
