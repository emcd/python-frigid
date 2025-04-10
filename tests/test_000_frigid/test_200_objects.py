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


''' Assert correct function of objects. '''


import pytest

from dataclasses import dataclass
from itertools import product

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.objects' ) )
THESE_CLASSES_NAMES = ( 'Object', )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    obj = Object( )
    assert isinstance( obj, Object )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_immutability( module_qname, class_name ):
    ''' Object prevents attribute modification after initialization. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )

    class Example( Object ):
        def __init__( self ):
            self.value = 42
            super( ).__init__( )

    obj = Example( )
    assert 42 == obj.value
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.value = -1
    assert 42 == obj.value
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.new_attr = 'test'
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.value


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_102_string_representation( module_qname, class_name ):
    ''' Object has expected string representations. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    obj = factory( )
    assert base.calculate_fqname( obj ) in repr( obj )


def test_200_immutable_decorator_basic( ):
    ''' Decorator makes regular class immutable. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class Example:
        def __init__( self ):
            self.value = 42

    obj = Example( )
    assert 42 == obj.value
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.value = 24
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.new_attr = 'test'
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.value


def test_201_immutable_decorator_with_dataclass( ):
    ''' Decorator works with dataclass. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    @dataclass( kw_only = True )
    class Example:
        x: int
        y: str = 'default'

    obj = Example( x = 42 )
    assert 42 == obj.x
    assert 'default' == obj.y
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.x = 24
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.y = 'changed'


def test_202_immutable_decorator_inheritance( ):
    ''' Decorator properly handles inheritance. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class Base:
        def __init__( self ):
            self.base_attr = 'base'
            super( ).__init__( )

    class Derived( Base ):
        def __init__( self ):
            self.derived_attr = 'derived'
            super( ).__init__( )

    obj = Derived( )
    assert 'base' == obj.base_attr
    assert 'derived' == obj.derived_attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.base_attr = 'modified'
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.derived_attr = 'modified'


def test_203_immutable_decorator_compatibility( ):
    ''' Decorator raises error for incompatible classes. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    with pytest.raises( exceptions.DecoratorCompatibilityError ):
        @module.immutable
        class BadExample:
            def __setattr__( self, name, value ):
                pass # pragma: no coverage

    with pytest.raises( exceptions.DecoratorCompatibilityError ):
        @module.immutable
        class AnotherBadExample:
            def __delattr__( self, name ):
                pass # pragma: no coverage


def test_204_immutable_decorator_slots( ):
    ''' Decorator handles classes with slots. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class Example:
        __slots__ = ( '_behaviors_', 'x', 'y' )

        def __init__( self ):
            self.x = 1
            self.y = 2

    obj = Example( )
    assert 1 == obj.x
    assert 2 == obj.y
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.x = 3
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.y = 4
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.x


def test_205_immutable_decorator_existing_behaviors( ):
    ''' Decorator handles classes with existing behaviors. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class DictExample:
        def __init__( self ):
            self._behaviors_ = { 'existing' }
            self.value = 42

    obj1 = DictExample( )
    assert 'existing' in obj1._behaviors_
    assert module.__.behavior_label in obj1._behaviors_
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj1.value = 24

    @module.immutable
    class SlotsExample:
        __slots__ = ( '_behaviors_', 'value' )

        def __init__( self ):
            self._behaviors_ = { 'existing' }
            self.value = 42

    obj2 = SlotsExample( )
    assert 'existing' in obj2._behaviors_
    assert module.__.behavior_label in obj2._behaviors_
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj2.value = 24


def test_206_immutable_decorator_mixed_slots_dict( ):
    ''' Decorator handles classes with both slots and dict. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class Example:
        __slots__ = ( '__dict__', 'x', 'y' )

        def __init__( self ):
            self.x = 1
            self.y = 2
            self.z = 3  # Goes to __dict__

    obj = Example( )
    assert 1 == obj.x
    assert 2 == obj.y
    assert 3 == obj.z
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.x = 4
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.z = 4


def test_207_immutable_decorator_initialization_deletion( ):
    ''' Decorator allows deletion during initialization. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class Example:
        __slots__ = ( '_behaviors_', 'x' )

        def __init__( self ):
            self.x = 1
            del self.x

    obj = Example( )
    with pytest.raises( AttributeError ):
        _ = obj.x
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj._behaviors_


def test_210_immutable_decorator_with_parameters( ):
    ''' Decorator accepts and applies parameters correctly. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    # Test with docstring parameter
    custom_doc = 'This is a custom docstring'

    @module.immutable( docstring = custom_doc )
    class WithDocstring:
        ''' Original docstring '''
        def __init__( self ):
            self.attr = 'test'

    assert custom_doc == WithDocstring.__doc__

    # Test with mutables parameter
    @module.immutable( mutables = ( 'version', ) )
    class WithMutables:
        def __init__( self ):
            self.name = 'test'
            self.version = '1.0.0'

    obj = WithMutables( )
    # Mutable attribute can be changed
    obj.version = '2.0.0'
    assert '2.0.0' == obj.version

    # Non-mutable attribute cannot be changed
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.name = 'changed'


def test_211_immutable_decorator_function_form( ):
    ''' Decorator works when called as a function with parameters. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    # Create decorator with parameters
    decorator = module.immutable(
        mutables = ( 'version', ),
        docstring = 'Decorated class'
    )

    # Apply it to a class
    @decorator
    class Config:
        def __init__( self, name, version ):
            self.name = name
            self.version = version

    # Test behavior
    config = Config( 'TestApp', '1.0.0' )

    # Mutable attribute
    config.version = '2.0.0'
    assert '2.0.0' == config.version

    # Immutable attribute
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        config.name = 'NewName'

    # Docstring set correctly
    assert 'Decorated class' == Config.__doc__


def test_212_immutable_with_nested_objects( ):
    ''' Immutable decorator properly handles nested object attributes. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    class InnerClass:
        def __init__( self ):
            self.value = 42

    @module.immutable
    class OuterClass:
        def __init__( self ):
            self.inner = InnerClass( )
            self.name = 'outer'

    # Create instance
    obj = OuterClass( )

    # Outer object is immutable
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.name = 'changed'

    # Inner object's attributes can still be changed
    # since the immutability is not recursive
    obj.inner.value = 100
    assert 100 == obj.inner.value

    # But the inner object reference cannot be changed
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.inner = InnerClass( )


def test_213_immutable_initialization_edge_cases( ):
    ''' Test edge cases for immutable object initialization. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable
    class DynamicInit:
        def __init__( self, **kwargs ):
            for key, value in kwargs.items( ):
                setattr( self, key, value )

    # Test with various initialization patterns
    obj1 = DynamicInit( a = 1, b = 2, c = 3 )
    assert 1 == obj1.a
    assert 2 == obj1.b
    assert 3 == obj1.c

    # Cannot modify after initialization
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj1.a = 10

    # Another initialization pattern
    obj2 = DynamicInit( **{ 'x': 100, 'y': 200 } )
    assert 100 == obj2.x
    assert 200 == obj2.y

    # Cannot add new attributes
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj2.z = 300

def test_214_immutable_decorator_delete_mutable( ):
    ''' Test deletion of mutable attributes in immutable objects. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )

    @module.immutable( mutables = ( 'can_delete', ) )
    class Example:
        def __init__( self ):
            self.value = 42
            self.can_delete = 'temporary'

    obj = Example( )

    # Should be able to delete the mutable attribute
    assert hasattr( obj, 'can_delete' )
    del obj.can_delete
    assert not hasattr( obj, 'can_delete' )

    # Still can't delete immutable attributes
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.value


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Class has valid docstring. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    assert hasattr( Object, '__doc__' )
    assert isinstance( Object.__doc__, str )
    assert Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_902_docstring_mentions_immutability( module_qname, class_name ):
    ''' Class docstring mentions immutability. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'instance attributes immutability' )
    assert fragment in Object.__doc__
