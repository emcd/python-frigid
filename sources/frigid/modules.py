# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Immutable modules.

    Provides a module type that enforces complete attribute immutability.
    This helps ensure that module-level constants remain constant and that
    module interfaces remain stable during runtime.

    The module implementation is derived from :py:class:`types.ModuleType` and
    adds immutability. This makes it particularly useful for:

    * Ensuring constants remain constant
    * Preventing modification of module interfaces

    Also provides a convenience function:

    * ``reclassify_modules``: Converts existing modules to immutable modules.
'''


from . import __
from . import classes as _classes


class Module( _classes.Object, __.types.ModuleType ):
    ''' Modules with attributes immutability and concealment. '''

    # TODO: Dynadoc fragments.


reclassify_modules = (
    __.funct.partial(
        __.ccstd.reclassify_modules,
        attributes_namer = __.calculate_attrname,
        replacement_class = Module ) )
