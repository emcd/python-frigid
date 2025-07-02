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


''' Assert correct function of internal dictionaries. '''


import pytest

from types import MappingProxyType as DictionaryProxy

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__"

dictionary_posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
dictionary_nomargs = DictionaryProxy( dict( orb = False ) )


def test_200_immutable_dictionary_instantiation( ):
    ''' Dictionary instantiates with various input types. '''
    module = cache_import_module( MODULE_QNAME )
    factory = module.ImmutableDictionary
    dct1 = factory( )
    assert isinstance( dct1, factory )
    dct2 = factory( *dictionary_posargs, **dictionary_nomargs )
    assert isinstance( dct2, factory )
    assert 1 == dct2[ 'foo' ]
    assert 2 == dct2[ 'bar' ]
    assert dct2[ 'unicorn' ]
    assert not dct2[ 'orb' ]
    assert ( 'foo', 'bar', 'unicorn', 'orb' ) == tuple( dct2.keys( ) )
    assert ( 1, 2, True, False ) == tuple( dct2.values( ) )


def test_201_immutable_dictionary_duplication( ):
    ''' Dictionary is duplicable. '''
    module = cache_import_module( MODULE_QNAME )
    factory = module.ImmutableDictionary
    odct = factory( *dictionary_posargs, **dictionary_nomargs )
    ddct = odct.copy( )
    assert odct == ddct
    assert id( odct ) != id( ddct )


def test_202_immutable_dictionary_prevents_key_overwrite( ):
    ''' Dictionary prevents overwriting existing keys during creation. '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.__.exceptions" )
    with pytest.raises( exceptions.EntryImmutability ):
        module.ImmutableDictionary( [ ( 'a', 1 ) ], { 'a': 2 } )


def test_210_immutable_dictionary_entry_protection( ):
    ''' Dictionary prevents entry modification and deletion. '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.__.exceptions" )
    factory = module.ImmutableDictionary
    dct = factory( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.EntryImmutability ):
        dct[ 'foo' ] = 42
    with pytest.raises( exceptions.EntryImmutability ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.EntryImmutability ):
        dct[ 'baz' ] = 3.1415926535


def test_211_immutable_dictionary_operation_prevention( ):
    ''' Dictionary prevents all mutating operations. '''
    module = cache_import_module( MODULE_QNAME )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.__.exceptions" )
    factory = module.ImmutableDictionary
    dct = factory( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.OperationInvalidity ):
        dct.clear( )
    with pytest.raises( exceptions.OperationInvalidity ):
        dct.pop( 'foo' )
    with pytest.raises( exceptions.OperationInvalidity ):
        dct.pop( 'foo', default = -1 )
    with pytest.raises( exceptions.OperationInvalidity ):
        dct.popitem( )
    with pytest.raises( exceptions.OperationInvalidity ):
        dct.update( baz = 42 )


def test_212_immutable_dictionary_initialization_validation( ):
    ''' Dictionary properly handles various input types during creation. '''
    module = cache_import_module( MODULE_QNAME )
    factory = module.ImmutableDictionary
    dct1 = factory( { 'a': 1, 'b': 2 } )
    assert 1 == dct1[ 'a' ]
    assert 2 == dct1[ 'b' ]
    dct2 = factory( [ ( 'c', 3 ), ( 'd', 4 ) ] )
    assert 3 == dct2[ 'c' ]
    assert 4 == dct2[ 'd' ]
    dct3 = factory( e = 5, f = 6 )
    assert 5 == dct3[ 'e' ]
    assert 6 == dct3[ 'f' ]
    dct4 = factory( { 'g': 7 }, [ ( 'h', 8 ) ], i = 9 )
    assert 7 == dct4[ 'g' ]
    assert 8 == dct4[ 'h' ]
    assert 9 == dct4[ 'i' ]


def test_213_immutable_dictionary_behaviors( ):
    ''' Dictionary has proper immutability behavior. '''
    module = cache_import_module( MODULE_QNAME )
    factory = module.ImmutableDictionary
    dct = factory( a = 1 )
    assert module.dictionaries._immutability_label in dct._behaviors_
