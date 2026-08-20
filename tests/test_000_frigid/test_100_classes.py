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


_frigid = cache_import_module( PACKAGE_NAME )


class _Regular( _frigid.Protocol ): pass
class _Data( _frigid.DataclassProtocol ): pass
class _Combined( _Data, _Regular ): pass


def test_100_provide_error_class_failure():
    ''' Error provider raises for unknown error names. '''
    classes_module = cache_import_module( f"{PACKAGE_NAME}.classes" )
    exceptions_module = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    
    with pytest.raises( exceptions_module.ErrorProvideFailure ) as exc_info:
        classes_module._provide_error_class( 'NonExistentError' )
    
    message = str( exc_info.value )
    assert 'NonExistentError' in message
    assert 'Does not exist' in message


def test_200_protocol_metaclass_hierarchy():
    ''' Protocol metaclass hierarchy matches classcore pattern. '''
    classes_module = cache_import_module( f"{PACKAGE_NAME}.classes" )
    assert issubclass(
        classes_module.ProtocolDataclass, classes_module.ProtocolClass )
    assert issubclass(
        classes_module.ProtocolDataclassMutable,
        classes_module.ProtocolDataclass )
    assert issubclass(
        classes_module.ProtocolDataclassMutable,
        classes_module.ProtocolClass )


def test_201_protocol_metaclass_mro():
    ''' Protocol metaclass MRO includes parent chain. '''
    classes_module = cache_import_module( f"{PACKAGE_NAME}.classes" )
    mro = classes_module.ProtocolDataclassMutable.__mro__
    mro_names = [ c.__name__ for c in mro ]
    assert mro_names.index( 'ProtocolDataclassMutable' ) < \
           mro_names.index( 'ProtocolDataclass' )
    assert mro_names.index( 'ProtocolDataclass' ) < \
           mro_names.index( 'ProtocolClass' )


def test_202_protocol_metaclass_composability():
    ''' Dataclass protocol can inherit from protocol class.

    This is the Ictr use case: a protocol class (ProtocolClass
    metaclass) and a dataclass protocol (ProtocolDataclass metaclass)
    that inherits from it. Before the hierarchy alignment, this raised
    TypeError: metaclass conflict.
    '''
    assert type( _Combined ) is _frigid.ProtocolDataclass
    assert issubclass( _Combined, _Regular )
