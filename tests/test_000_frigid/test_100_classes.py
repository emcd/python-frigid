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


_TYPING_MACHINERY_NAMES = (
    '_is_runtime_protocol',
    '__non_callable_proto_members__',
    '__typing_is_deprecated_inherited_runtime_protocol__',
)
_ABC_MACHINERY_NAMES = (
    '_abc_cache',
    '_abc_negative_cache',
    '_abc_negative_cache_version',
    '_abc_registry',
)
_PROTOCOL_BASES_NAMES = (
    'Protocol',
    'ProtocolMutable',
    'DataclassProtocol',
    'DataclassProtocolMutable',
)


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


@pytest.mark.parametrize( 'base_name', _PROTOCOL_BASES_NAMES )
@pytest.mark.parametrize( 'name', _TYPING_MACHINERY_NAMES )
def test_300_typing_machinery_names_assignable( base_name, name ):
    ''' Typing machinery names remain assignable on protocol bases.

        CPython 3.15+ typing sets
        '__typing_is_deprecated_inherited_runtime_protocol__' during class
        decoration and again in the 'runtime_checkable' decorator. The
        '_is_runtime_protocol' and '__non_callable_proto_members__' names
        are set by 'runtime_checkable'. All three must survive class-level
        immutability, which is what the typing_class_mutables exemption
        provides.
    '''
    base = getattr( _frigid, base_name )
    cls = type( f"_Probe{base_name}", ( base, ), { } )
    setattr( cls, name, True )
    assert cls.__dict__[ name ] is True


@pytest.mark.parametrize( 'base_name', _PROTOCOL_BASES_NAMES )
@pytest.mark.parametrize( 'name', _ABC_MACHINERY_NAMES )
def test_301_abc_machinery_names_assignable( base_name, name ):
    ''' ABC machinery names remain assignable on protocol bases. '''
    base = getattr( _frigid, base_name )
    cls = type( f"_Probe{base_name}", ( base, ), { } )
    setattr( cls, name, True )
    assert cls.__dict__[ name ] is True


@pytest.mark.parametrize( 'base_name', _PROTOCOL_BASES_NAMES )
def test_302_ordinary_names_remain_immutable( base_name ):
    ''' Class-level immutability still rejects ordinary names.

        Exempting the typing and ABC machinery must not weaken immutability
        for anything else.
    '''
    exceptions_module = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    base = getattr( _frigid, base_name )
    cls = type( f"_Probe{base_name}", ( base, ), { } )
    with pytest.raises( exceptions_module.AttributeImmutability ) as exc_info:
        setattr( cls, 'ordinary', True )
    assert 'ordinary' in str( exc_info.value )
    assert base_name in str( exc_info.value )
