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


''' Assert correct function of nomina utilities. '''


import pytest

from . import PACKAGE_NAME, cache_import_module


@pytest.mark.parametrize( 'name,expected', [
    ( 'public_name', True ),
    ( 'another_public', True ),
    ( 'CamelCase', True ),
    ( 'snake_case', True ),
    ( 'single', True ),
    ( '_private_name', False ),
    ( '__dunder__', False ),
    ( '__private', False ),
    ( '_', False ),
    ( '__class__', False ),
])
def test_100_is_public_identifier( name, expected ):
    ''' Function correctly identifies public identifiers. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    assert module.is_public_identifier( name ) is expected