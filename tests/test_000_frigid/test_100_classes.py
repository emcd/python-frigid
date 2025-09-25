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


''' Assert correct function of classes module. '''


import pytest

from .__ import PACKAGE_NAME, cache_import_module


def test_100_provide_error_class_failure():
    ''' Error provider raises for unknown error names. '''
    classes_module = cache_import_module( f"{PACKAGE_NAME}.classes" )
    exceptions_module = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    
    with pytest.raises( exceptions_module.ErrorProvideFailure ) as exc_info:
        classes_module._provide_error_class( 'NonExistentError' )
    
    message = str( exc_info.value )
    assert 'NonExistentError' in message
    assert 'Does not exist' in message