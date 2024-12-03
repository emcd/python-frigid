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


''' Assert correct function of dictionaries. '''

# mypy: ignore-errors
# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name,magic-value-comparison,protected-access
# pylint: disable=too-many-locals,too-many-statements,unnecessary-dunder-call


import pytest

from itertools import product
from types import MappingProxyType as DictionaryProxy

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.dictionaries' ) )
THESE_CLASSES_NAMES = ( 'Dictionary', 'ValidatorDictionary' )
VALIDATOR_NAMES = ( 'ValidatorDictionary', )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


def select_arguments( class_name ):
    ''' Chooses initializer arguments depending on class. '''
    if class_name in VALIDATOR_NAMES:
        return ( lambda k, v: isinstance( v, int ), ), { }
    return ( ), { }


def select_simple_arguments( class_name ):
    ''' Choose simple test arguments depending on class. '''
    posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
    nomargs = DictionaryProxy( dict( orb = False ) )
    if class_name in VALIDATOR_NAMES:
        posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': 42 } )
        nomargs = DictionaryProxy( dict( orb = 84 ) )
    return posargs, nomargs


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert isinstance( dct, factory )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *posargs, *simple_posargs, **simple_nomargs )
    assert isinstance( dct, factory )
    assert 1 == dct[ 'foo' ]
    assert 2 == dct[ 'bar' ]
    assert (
        dct[ 'unicorn' ] if class_name == 'Dictionary'
        else dct[ 'unicorn' ] == 42 )
    assert (
        not dct[ 'orb' ] if class_name == 'Dictionary'
        else dct[ 'orb' ] == 84 )
    assert ( 'bar', 'foo', 'orb', 'unicorn' ) == tuple( sorted( dct.keys( ) ) )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, VALIDATOR_NAMES )
)
def test_102_instantiation( module_qname, class_name ):
    ''' Validator class instantiates. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert isinstance( dct, factory )
    with pytest.raises( exceptions.EntryValidityError ):
        dct = factory( *posargs, invalid = 'str' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_attribute_immutability( module_qname, class_name ):
    ''' Dictionary attributes are immutable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    obj = factory( *posargs, **nomargs )
    with pytest.raises( AttributeError ):
        obj.attr = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_200_dictionary_entry_immutability( module_qname, class_name ):
    ''' Dictionary entries are immutable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *posargs, *simple_posargs, **simple_nomargs )
    with pytest.raises( exceptions.EntryImmutabilityError ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.EntryImmutabilityError ):
        dct[ 'foo' ] = 666
    with pytest.raises( exceptions.EntryImmutabilityError ):
        dct[ 'baz' ] = 43


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_160_or_combines_dictionaries( module_qname, class_name ):
    ''' Dictionary union produces new dictionary with combined entries. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, a = 1 )
    d2 = factory( *posargs, c = 4 )
    d3 = { 'd': 5, 'e': 6 }
    d4 = d1 | d2
    assert isinstance( d4, factory )
    assert d4 == { 'a': 1, 'c': 4 }
    d5 = d1 | d3
    assert isinstance( d5, factory )
    assert d5 == { 'a': 1, 'd': 5, 'e': 6 }
    d6 = d3 | d1
    assert isinstance( d6, factory )
    assert d6 == { 'a': 1, 'd': 5, 'e': 6 }
    d7 = factory( *posargs, a = 2 )
    d8 = d1 | d7
    assert d8 == { 'a': 2 }


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_161_or_rejects_invalid_operands( module_qname, class_name ):
    ''' Dictionary union rejects non-mapping operands. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert NotImplemented == dct.__or__( [ ] )
    assert NotImplemented == dct.__ror__( [ ] )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_170_and_intersects_mappings( module_qname, class_name ):
    ''' Dictionary intersection with mapping matches key-value pairs. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, a = 1, b = 2, c = 3 )
    d2 = factory( *posargs, a = 1, b = 3, d = 4 )
    d3 = { 'a': 1, 'c': 3, 'e': 5 }
    d4 = d1 & d2
    assert isinstance( d4, factory )
    assert d4 == { 'a': 1 }
    d5 = d1 & d3
    assert isinstance( d5, factory )
    assert d5 == { 'a': 1, 'c': 3 }
    d6 = d3 & d1
    assert isinstance( d6, factory )
    assert d6 == { 'a': 1, 'c': 3 }


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_171_and_filters_by_keys( module_qname, class_name ):
    ''' Dictionary intersection with set filters by keys. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, a = 1, b = 2, c = 3 )
    s1 = { 'a', 'b' }
    d2 = d1 & s1
    assert isinstance( d2, factory )
    assert d2 == { 'a': 1, 'b': 2 }
    d3 = d1 & factory( *posargs, x = 0, a = 9, b = 8 ).keys( )
    assert isinstance( d3, factory )
    assert d3 == { 'a': 1, 'b': 2 }
    d4 = s1 & d1
    assert isinstance( d4, factory )
    assert d4 == { 'a': 1, 'b': 2 }


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_172_and_rejects_invalid_operands( module_qname, class_name ):
    ''' Dictionary intersection rejects invalid operands. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, **nomargs )
    assert NotImplemented == dct.__and__( [ ] )
    assert NotImplemented == dct.__rand__( [ ] )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, VALIDATOR_NAMES )
)
def test_202_validator_dictionary_validation( module_qname, class_name ):
    ''' Validator dictionary validates entries during creation. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    dct = factory( *posargs, valid = 42 )
    with pytest.raises( exceptions.EntryValidityError ):
        factory( *posargs, invalid = 'str' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_220_duplication( module_qname, class_name ):
    ''' Dictionary is duplicable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    odct = factory( *posargs, a = 1, b = 2 )
    ddct = odct.copy( )
    assert odct == ddct
    assert odct is not ddct


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_221_dictionary_iterability( module_qname, class_name ):
    ''' Dictionary is iterable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *posargs, *simple_posargs, **simple_nomargs )
    assert frozenset( dct.keys( ) ) == frozenset( iter( dct ) )
    assert tuple( dct.items( ) ) == tuple( zip( dct.keys( ), dct.values( ) ) )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_222_dictionary_measurability( module_qname, class_name ):
    ''' Dictionary is measurable. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *posargs, *simple_posargs, **simple_nomargs )
    assert len( dct.keys( ) ) == len( dct )
    assert len( dct.items( ) ) == len( dct )
    assert len( dct.values( ) ) == len( dct )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_225_dictionary_equality( module_qname, class_name ):
    ''' Dictionary is equivalent to another dictionary with same values. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct1 = factory( *posargs, *simple_posargs, **simple_nomargs )
    dct2 = dct1.copy( )
    dct3 = dict( dct1 )
    assert dct1 == dct2
    assert dct2 == dct1
    assert dct1 == dct3
    assert dct3 == dct1
    assert not ( dct1 == -1 )
    assert dct1 != -1
    assert dct1 != ( )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_230_string_representation( module_qname, class_name ):
    ''' Dictionary has expected string representations. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *posargs, *simple_posargs, **simple_nomargs )
    cdct = dict( dct )
    assert str( cdct ) == str( dct )
    assert str( cdct ) in repr( dct )
    assert base.calculate_fqname( dct ) in repr( dct )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_240_dictionary_entry_optional_retrieval( module_qname, class_name ):
    ''' Default value on optional access of dictionary entry. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    simple_posargs, simple_nomargs = select_simple_arguments( class_name )
    dct = factory( *posargs, *simple_posargs, **simple_nomargs )
    assert None is dct.get( 'baz' )
    assert -1 == dct.get( 'baz', -1 )
    assert -1 == dct.get( 'baz', default = -1 )
    assert 1 == dct.get( 'foo' )
    assert 1 == dct.get( 'foo', -1 )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_250_with_data( module_qname, class_name ):
    ''' Dictionary creates new instance with different data. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    posargs, nomargs = select_arguments( class_name )
    d1 = factory( *posargs, a = 1, b = 2 )
    new_data = { 'c': 3, 'd': 4 }
    d2 = d1.with_data( new_data )
    assert isinstance( d2, factory )
    assert type( d1 ) is type( d2 )
    assert d1 != d2
    assert d2 == { 'c': 3, 'd': 4 }
    if class_name in VALIDATOR_NAMES:
        with pytest.raises( exceptions.EntryValidityError ):
            d2 = d1.with_data( invalid = 'str' )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_260_subclasses_abc_dictionary( module_qname, class_name ):
    ''' Subclasses 'collections.abc.Mapping'. '''
    from collections.abc import Mapping as AbstractDictionary
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    assert issubclass( factory, AbstractDictionary )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Class has valid docstring. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    assert hasattr( factory, '__doc__' )
    assert isinstance( factory.__doc__, str )
    assert factory.__doc__
