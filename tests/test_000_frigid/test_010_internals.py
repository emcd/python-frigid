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


''' Assert correct function of internals. '''

# mypy: ignore-errors
# pylint: disable=attribute-defined-outside-init
# pylint: disable=magic-value-comparison
# pylint: disable=missing-class-docstring
# pylint: disable=protected-access
# ruff: noqa: E711,E712


import pytest

from platform import python_implementation
from types import MappingProxyType as DictionaryProxy

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__"
MODULE_ATTRIBUTE_NAMES = (
    'Absent',
    'ConcealerExtension',
    'Docstring',
    'Falsifier',
    'InternalClass',
    'InternalObject',
    #'absent',
    'calculate_class_fqname',
    'calculate_fqname',
    'discover_public_attributes',
    'generate_docstring',
)

exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
module = cache_import_module( MODULE_QNAME )

dictionary_posargs = ( ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True } )
dictionary_nomargs = DictionaryProxy( dict( orb = False ) )

pypy_skip_mark = pytest.mark.skipif(
    'PyPy' == python_implementation( ),
    reason = "PyPy handles class cell updates differently"
)


def test_102_concealer_extension_attribute_visibility( ):
    ''' Instance conceals attributes according to visibility rules. '''
    obj = module.ConcealerExtension( )
    obj.public = 42
    assert ( 'public', ) == tuple( dir( obj ) )
    obj._hidden = 24
    assert ( 'public', ) == tuple( dir( obj ) )
    obj._visible = 12
    obj._attribute_visibility_includes_ = frozenset( ( '_visible', ) )
    assert ( '_visible', 'public' ) == tuple( sorted( dir( obj ) ) )


def test_111_internal_class_immutability( ):
    ''' Class attributes become immutable after initialization. '''
    factory = module.InternalClass
    class Example( metaclass = factory ): value = 42
    with pytest.raises( AttributeError ): Example.value = 24
    with pytest.raises( AttributeError ): del Example.value


def test_112_internal_class_decorator_handling( ):
    ''' Class properly handles decorators during creation. '''
    factory = module.InternalClass
    def decorator1( cls ):
        cls.attr1 = 'one'
        return cls
    def decorator2( cls ):
        cls.attr2 = 'two'
        return cls

    class Example(
        metaclass = factory, decorators = ( decorator1, decorator2 )
    ): pass

    assert 'one' == Example.attr1
    assert 'two' == Example.attr2 # pylint: disable=no-member
    with pytest.raises( AttributeError ): Example.attr1 = 'changed'


def test_113_internal_class_attribute_visibility( ):
    ''' Class conceals attributes according to visibility rules. '''
    factory = module.InternalClass

    class Example( metaclass = factory ):
        _class_attribute_visibility_includes_ = frozenset( ( '_visible', ) )
        public = 42
        _hidden = 24
        _visible = 12

    assert ( '_visible', 'public' ) == tuple( sorted( dir( Example ) ) )


@pypy_skip_mark
def test_114_internal_class_decorator_replacement( ):
    ''' Class properly handles decorators that return new classes. '''
    from dataclasses import dataclass
    factory = module.InternalClass

    class Example(
        metaclass = factory, decorators = ( dataclass( slots = True ), )
    ):
        field1: str
        field2: int

    assert hasattr( Example, '__slots__' )
    with pytest.raises( AttributeError ): Example.field1 = 'changed'


def test_115_internal_class_behaviors_extension( ):
    ''' Class properly extends existing behaviors. '''
    factory = module.InternalClass

    class Base( metaclass = factory ):
        _class_behaviors_ = { 'existing' }

    assert 'existing' in Base._class_behaviors_
    assert module.behavior_label in Base._class_behaviors_


def test_116_internal_class_nested_visibility( ):
    ''' Class properly handles visibility in nested hierarchies. '''
    factory = module.InternalClass

    class Base( metaclass = factory ):
        _class_attribute_visibility_includes_ = (
            frozenset( ( '_base_visible', ) ) )
        _base_visible = 'visible'
        _base_hidden = 'hidden'

    class Derived( Base ):
        _class_attribute_visibility_includes_ = (
            frozenset( ( '_derived_visible', ) ) )
        _derived_visible = 'visible'
        _derived_hidden = 'hidden'

    assert ( '_base_visible', '_derived_visible' ) == tuple(
        sorted( name for name in dir( Derived )
        if name.startswith( '_' ) ) )

@pypy_skip_mark
def test_117_internal_class_complex_decorator( ):
    ''' Class properly handles complex decorator scenarios. '''
    from dataclasses import dataclass
    from typing import ClassVar
    factory = module.InternalClass

    def add_class_var( cls ):
        cls.class_var = 'added'
        return cls

    @dataclass
    class Mixin:
        field3: str = 'mixin'  # Optional field with default

    class Example(
        Mixin,
        metaclass = factory,
        decorators = (
            dataclass( kw_only = True, slots = True ),
            add_class_var,
        )
    ):
        field1: str
        field2: int
        const: ClassVar[str] = 'const'

    obj = Example( field1 = 'test', field2 = 42 )  # field3 uses default
    assert 'test' == obj.field1
    assert 42 == obj.field2
    assert 'mixin' == obj.field3
    assert 'const' == Example.const
    assert 'added' == Example.class_var
    with pytest.raises( AttributeError ):
        Example.class_var = 'modified'


def test_150_internal_object_immutability( ):
    ''' Instance attributes cannot be modified or deleted. '''
    class Example( module.InternalObject ):
        def __init__( self ):
            # Need to bypass normal setattr to initialize
            super( module.InternalObject, self ).__setattr__( 'value', 42 )

    obj = Example( )
    with pytest.raises( AttributeError ): obj.value = 24
    with pytest.raises( AttributeError ): obj.new_attr = 'test'
    with pytest.raises( AttributeError ): del obj.value


def test_160_falsifier_behavior( ):
    ''' Falsifier objects are falsey and compare properly. '''
    class Example( module.Falsifier ): pass

    obj1 = Example( )
    obj2 = Example( )
    assert not obj1
    assert obj1 == obj1 # pylint: disable=comparison-with-itself
    assert obj1 != obj2
    assert obj1 is not True
    assert obj1 is not False
    assert obj1 is not None


def test_170_absent_singleton( ):
    ''' Absent class produces singleton instance. '''
    obj1 = module.Absent( )
    obj2 = module.Absent( )
    assert obj1 is obj2
    assert obj1 is module.absent
    assert not obj1
    assert obj1 == obj1 # pylint: disable=comparison-with-itself
    assert obj1 != None # pylint: disable=singleton-comparison
    assert obj1 != False # pylint: disable=singleton-comparison


def test_172_absent_type_guard_edge_cases( ):
    ''' Type guard handles edge cases properly. '''

    def example( value: module.Optional[ str ] ) -> str:
        if not module.is_absent( value ): return value
        return 'default'

    # Test with various falsey values
    assert '' == example( '' )
    assert '0' == example( '0' )
    assert 'False' == example( 'False' )
    assert 'None' == example( 'None' )
    # Test with various truthy values
    assert 'test' == example( 'test' )
    assert '42' == example( '42' )
    assert 'True' == example( 'True' )
    # Test for absence.
    assert 'default' == example( module.absent )


def test_200_immutable_dictionary_instantiation( ):
    ''' Dictionary instantiates with various input types. '''
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
    factory = module.ImmutableDictionary
    odct = factory( *dictionary_posargs, **dictionary_nomargs )
    ddct = odct.copy( )
    assert odct == ddct
    assert id( odct ) != id( ddct )


def test_202_immutable_dictionary_prevents_key_overwrite( ):
    ''' Dictionary prevents overwriting existing keys during creation. '''
    with pytest.raises( exceptions.EntryImmutabilityError ):
        module.ImmutableDictionary( [ ( 'a', 1 ) ], { 'a': 2 } )


def test_210_immutable_dictionary_entry_protection( ):
    ''' Dictionary prevents entry modification and deletion. '''
    factory = module.ImmutableDictionary
    dct = factory( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.EntryImmutabilityError ):
        dct[ 'foo' ] = 42
    with pytest.raises( exceptions.EntryImmutabilityError ):
        del dct[ 'foo' ]
    with pytest.raises( exceptions.EntryImmutabilityError ):
        dct[ 'baz' ] = 3.1415926535


def test_211_immutable_dictionary_operation_prevention( ):
    ''' Dictionary prevents all mutating operations. '''
    factory = module.ImmutableDictionary
    dct = factory( *dictionary_posargs, **dictionary_nomargs )
    with pytest.raises( exceptions.OperationValidityError ):
        dct.clear( )
    with pytest.raises( exceptions.OperationValidityError ):
        dct.pop( 'foo' )
    with pytest.raises( exceptions.OperationValidityError ):
        dct.pop( 'foo', default = -1 )
    with pytest.raises( exceptions.OperationValidityError ):
        dct.popitem( )
    with pytest.raises( exceptions.OperationValidityError ):
        dct.update( baz = 42 )


def test_212_immutable_dictionary_initialization_validation( ):
    ''' Dictionary properly handles various input types during creation. '''
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
    factory = module.ImmutableDictionary
    dct = factory( a = 1 )
    assert module.behavior_label in dct._behaviors_


def test_171_absent_type_guard( ):
    ''' Type guard correctly identifies absent values. '''
    def example( value: module.Optional[ str ] ) -> str:
        if not module.is_absent( value ): return value
        return 'default'

    assert 'test' == example( 'test' )
    assert 'default' == example( module.absent )


def test_300_fqname_discovery( ):
    ''' Fully-qualified name of object is discovered. '''
    assert 'builtins.NoneType' == module.calculate_fqname( None )
    assert (
        'builtins.type'
        == module.calculate_fqname( module.ConcealerExtension ) )
    obj = module.ConcealerExtension( )
    assert (
        f"{MODULE_QNAME}.ConcealerExtension"
        == module.calculate_fqname( obj ) )


@pytest.mark.parametrize(
    'provided, expected',
    (
        ( { 'foo': 12 }, ( ) ),
        ( { '_foo': cache_import_module }, ( ) ),
        (
            { name: getattr( module, name )
              for name in MODULE_ATTRIBUTE_NAMES },
            MODULE_ATTRIBUTE_NAMES
        ),
    )
)
def test_400_public_attribute_discovery( provided, expected ):
    ''' Public attributes are discovered from dictionary. '''
    assert expected == module.discover_public_attributes( provided )


def test_500_docstring_generation_argument_acceptance( ):
    ''' Docstring generator errors on invalid arguments. '''
    class Foo: pass # pylint: disable=missing-class-docstring
    with pytest.raises( KeyError ):
        module.generate_docstring( 1 )
    with pytest.raises( KeyError ):
        module.generate_docstring( '8-bit theater' )
    assert not module.generate_docstring( Foo )
    assert module.generate_docstring( 'instance attributes immutability' )
    assert module.generate_docstring( module.Docstring( 'foo bar' ) )


def test_501_docstring_generation_validity( ):
    ''' Generated docstrings are correctly formatted. '''
    from inspect import getdoc

    class Foo:
        ''' headline

            additional information
        '''

    docstring_generated = module.generate_docstring(
        Foo,
        module.Docstring( 'foo bar' ),
        'class attributes immutability' )
    docstring_expected = '\n\n'.join( (
        getdoc( Foo ),
        'foo bar',
        module.generate_docstring( 'class attributes immutability' ) ) )
    assert docstring_expected == docstring_generated
