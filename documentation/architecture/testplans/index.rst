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


*******************************************************************************
Test Plans
*******************************************************************************

.. toctree::
   :maxdepth: 2

   summary

Test Structure
===============================================================================

Tests mirror the source package structure:

.. code-block::

    tests/
    ├── test_000_modules/           # Module-level tests
    │   ├── test_010_classes.py     # Tests for classes.py
    │   ├── test_020_dictionaries.py # Tests for dictionaries.py
    │   ├── test_030_namespaces.py  # Tests for namespaces.py
    │   ├── test_040_sequences.py   # Tests for sequences.py
    │   └── test_050_modules.py     # Tests for modules.py
    ├── test_100_edge_cases/        # Edge case and integration tests
    └── fixtures/                   # Shared test fixtures

Naming Conventions
-------------------------------------------------------------------------------

**File naming**: ``test_<priority>_<module>.py``

* Priority indicates test execution order (000, 010, 020, etc.)
* Module name matches the source module being tested

**Test function naming**: ``test_<number>_<description>``

* Number indicates test execution order within file
* Description uses snake_case and clearly states what is tested

Coverage Targets
-------------------------------------------------------------------------------

* >95% line coverage for source code
* 100% coverage of public API surface
* All documented examples tested via doctest