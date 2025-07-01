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
Frigid Modules
*******************************************************************************


Introduction
===============================================================================

The ``frigid.modules`` submodule provides functionality to enhance Python
modules with immutability and concealment, with optional automatic
documentation generation. This is particularly useful for package authors who
want to prevent accidental modification of their module's public API while
providing rich documentation.

The module provides two main approaches:

1. **Module finalization** - combines documentation generation with
   reclassification in a single convenient function (recommended)
2. **Module reclassification** - converts standard modules to have immutable
   and concealed attributes (deprecated)


Module Finalization with Documentation
===============================================================================

The ``finalize_module`` function provides a convenient way to combine automatic
documentation generation (via Dynadoc integration) with module reclassification.
This is the recommended approach for most packages.

Basic Usage
-------------------------------------------------------------------------------

.. code-block:: python

    # mypackage/__init__.py
    import frigid

    from . import core
    from . import utils
    from . import exceptions

    # Finalize the module with documentation and reclassification
    frigid.finalize_module( __name__, recursive = True )

The ``finalize_module`` function will:

1. Generate comprehensive documentation for the module and its members using
   Dynadoc introspection
2. Apply any documentation fragments you provide
3. Reclassify the module and its submodules for immutability and concealment

Advanced Configuration
-------------------------------------------------------------------------------

For complex packages, you might want to configure different parts differently:

.. code-block:: python

    # mypackage/__init__.py
    import frigid

    # Configure main package with full documentation
    frigid.finalize_module(
        __name__,
        recursive = False  # Handle submodules individually
    )

    # Configure submodules with different settings
    frigid.finalize_module(
        f"{__name__}.core",
        recursive = True
    )

    frigid.finalize_module(
        f"{__name__}.utils",
        recursive = True
    )

This approach allows you to provide different documentation and
introspection settings for different parts of your package.


Best Practices
===============================================================================

Package-Level Application
-------------------------------------------------------------------------------

For most packages, apply ``finalize_module`` at the package level in your
``__init__.py`` file:

.. code-block:: python

    # mypackage/__init__.py
    import frigid

    # Package metadata
    __version__ = '1.0.0'

    # Import public API
    from .core import PublicClass, public_function
    from .utils import helper_function

    # Finalize the entire package
    frigid.finalize_module( __name__, recursive = True )

This pattern ensures that:

- Your package's public API is documented
- All modules in the package are immutable and concealed
- The entire package hierarchy is protected from accidental modification

The ``recursive = True`` parameter provides the same mass reclassification
behavior as the deprecated ``reclassify_modules`` function, but with the
added benefit of automatic documentation generation.

Error Handling
-------------------------------------------------------------------------------

When using module finalization, be aware that the resulting modules will raise
``AttributeImmutability`` exceptions if code attempts to modify them:

.. code-block:: python

    import frigid.exceptions

    # After finalization, this will raise an exception
    try:
        mypackage.core.some_function = lambda: "modified"
    except frigid.exceptions.AttributeImmutability as e:
        print( f"Cannot modify module: {e}" )

Design your package APIs to avoid dynamic modification after finalization.
If you need dynamic behavior, consider using configuration objects or factory
functions instead of direct module attribute modification.


Integration with Build Systems
===============================================================================

Module finalization integrates well with modern Python build systems. The
immutability ensures that your package's API surface is clearly defined and
cannot be accidentally modified at runtime.

For packages that use entry points or plugin systems, apply finalization after
all dynamic setup is complete:

.. code-block:: python

    # mypackage/__init__.py
    import frigid

    # Dynamic setup (plugin registration, etc.)
    _setup_plugins()
    _register_entry_points()

    # Final API definition
    from .api import *

    # Lock down the package
    frigid.finalize_module( __name__, recursive = True )

This ensures that your package initialization is complete before the
immutability protections are applied.


Module Reclassification (Deprecated)
===============================================================================

.. deprecated::
   The ``reclassify_modules`` function is deprecated. Use ``finalize_module``
   with ``recursive = True`` instead, which provides the same functionality
   along with automatic documentation generation.

The ``reclassify_modules`` function converts modules to use a custom module
class that provides immutability and concealment behaviors. For new code,
use ``finalize_module`` instead:

.. code-block:: python

    # Deprecated approach
    # frigid.reclassify_modules( __name__, recursive = True )

    # Recommended approach
    frigid.finalize_module( __name__, recursive = True )

The ``finalize_module`` function provides the same module protection behaviors
while also generating comprehensive documentation for your modules.
