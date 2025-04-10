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


''' Assert correct function of class factory classes. '''


from itertools import product
from platform import python_implementation

import pytest
import typing_extensions as typx

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.classes' ) )
THESE_CLASSES_NAMES = ( 'Class', 'ABCFactory', 'ProtocolClass' )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )

pypy_skip_mark = pytest.mark.skipif(
    'PyPy' == python_implementation( ),
    reason = "PyPy handles class cell updates differently"
)


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''

    assert isinstance( Object, class_factory_class )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_immutability( module_qname, class_name ):
    ''' Class attributes are immutable. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class ):
        ''' test '''
        attr = 42

    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Object.attr = -1
    assert 42 == Object.attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del Object.attr
    assert 42 == Object.attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Object.new_attr = 'foo'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_110_class_decorators( module_qname, class_name ):
    ''' Class accepts and applies decorators correctly. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    decorator_calls = [ ]

    def test_decorator1( cls ):
        decorator_calls.append( 'decorator1' )
        cls.decorator1_attr = 'value1'
        return cls

    def test_decorator2( cls ):
        decorator_calls.append( 'decorator2' )
        cls.decorator2_attr = 'value2'
        return cls

    class Object(
        metaclass = class_factory_class,
        decorators = ( test_decorator1, test_decorator2 )
    ):
        ''' test '''
        attr = 42

        _class_behaviors_: typx.ClassVar[ set[ str ] ] = { 'foo' }

    assert [ 'decorator1', 'decorator2' ] == decorator_calls
    assert 'value1' == Object.decorator1_attr
    assert 'value2' == Object.decorator2_attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Object.decorator1_attr = 'new_value'
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Object.decorator2_attr = 'new_value'


@pypy_skip_mark
@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_111_class_decorator_reproduction_method( module_qname, class_name ):
    ''' Class handles decorator reproduction with super() method. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    from dataclasses import dataclass

    class Object(
        metaclass = class_factory_class,
        decorators = ( dataclass( slots = True ), )
    ):
        ''' test '''
        value: str = 'test'

        def method_with_super( self ):
            ''' References class cell on CPython. '''
            super( ).__init__( )
            return self.__class__.__name__

        def other_method_with_super( self ):
            ''' References class cell on CPython. '''
            super( ).__init__( )
            return 'other'

    # Verify class was properly reproduced and both methods work
    obj = Object( )
    assert 'Object' == obj.method_with_super( )
    assert 'other' == obj.other_method_with_super( )


@pypy_skip_mark
@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_112_class_decorator_reproduction_property( module_qname, class_name ):
    ''' Class handles decorator reproduction with dotted access property. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    from dataclasses import dataclass

    class Object(
        metaclass = class_factory_class,
        decorators = ( dataclass( slots = True ), )
    ):
        ''' test '''
        value: str = 'test'

        @property
        def prop_with_class( self ):
            ''' References class cell on CPython. '''
            return self.__class__.__name__

        @property
        def other_prop_with_class( self ):
            ''' References class cell on CPython. '''
            return f"other_{self.__class__.__name__}"

    # Verify class was properly reproduced and both properties work
    obj = Object( )
    assert 'Object' == obj.prop_with_class
    assert 'other_Object' == obj.other_prop_with_class


@pypy_skip_mark
@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_113_class_decorator_reproduction_no_cell( module_qname, class_name ):
    ''' Class handles decorator reproduction with no class cell. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    from dataclasses import dataclass

    class Object(
        metaclass = class_factory_class,
        decorators = ( dataclass( slots = True ), )
    ):
        ''' test '''
        value: str = 'test'

        def method_without_cell( self ):
            ''' Operates without class cell on CPython. '''
            return 'no_cell'

    # Verify class was properly reproduced
    obj = Object( )
    assert 'no_cell' == obj.method_without_cell( )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_114_decorator_error_handling( module_qname, class_name ):
    ''' Class handles decorator errors appropriately. '''
    module = cache_import_module( module_qname )
    class_factory_class = (
        getattr( module, class_name ) )

    def failing_decorator( cls ):
        raise ValueError( "Decorator failure" )

    with pytest.raises( ValueError, match = "Decorator failure" ):
        class Object(
            metaclass = class_factory_class,
            decorators = ( failing_decorator, )
        ):
            ''' test '''


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_120_docstring_assignment( module_qname, class_name ):
    ''' Class has dynamically-assigned docstring. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object( metaclass = class_factory_class, docstring = 'dynamic' ):
        ''' test '''
        attr = 42

    assert 'test' != Object.__doc__
    assert 'dynamic' == Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_130_mutable_attributes( module_qname, class_name ):
    ''' Specified attributes remain mutable. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Object(
        metaclass = class_factory_class, mutables = ( 'mutable_attr', )
    ):
        ''' test '''
        mutable_attr = 42
        immutable_attr = 'fixed'

    Object.mutable_attr = -1
    assert -1 == Object.mutable_attr
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Object.immutable_attr = 'changed'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_131_mutable_inheritance( module_qname, class_name ):
    ''' Mutable attributes are inherited properly. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class Base(
        metaclass = class_factory_class, mutables = ( 'base_mutable', )
    ):
        ''' test base '''
        base_mutable = 'base'
        base_immutable = 'fixed'

    class Child( Base, mutables = ( 'child_mutable', ) ):
        ''' test child '''
        child_mutable = 'child'
        child_immutable = 'fixed'

    # Base class mutables remain mutable
    Base.base_mutable = 'changed_base'
    assert 'changed_base' == Base.base_mutable
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Base.base_immutable = 'attempt'

    # Child inherits base mutables and adds its own
    Child.base_mutable = 'inherited_changed'
    assert 'inherited_changed' == Child.base_mutable
    Child.child_mutable = 'child_changed'
    assert 'child_changed' == Child.child_mutable
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Child.child_immutable = 'attempt'
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Child.base_immutable = 'attempt'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_132_mutable_edge_cases( module_qname, class_name ):
    ''' Handle edge cases for mutable attributes. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    # Empty mutables collection
    class EmptyMutables( metaclass = class_factory_class, mutables = ( ) ):
        ''' test empty mutables '''
        attr = 42

    with pytest.raises( exceptions.AttributeImmutabilityError ):
        EmptyMutables.attr = -1

    # Non-existent attributes can be added if listed as mutable
    class NonExistentMutable(
        metaclass = class_factory_class,
        mutables = ( 'does_not_exist', 'another_future_attr' )
    ):
        ''' test non-existent mutable '''
        attr = 42

    # Should succeed because it's in mutables list
    NonExistentMutable.does_not_exist = 'new'
    assert 'new' == NonExistentMutable.does_not_exist

    # Should fail because it's not in mutables list
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        NonExistentMutable.not_in_mutables = 'attempt'

    # Special method names as mutable attributes
    class SpecialMutable(
        metaclass = class_factory_class,
        mutables = ( '__special__', )
    ):
        ''' test special method mutable '''
        __special__ = None

    SpecialMutable.__special__ = 42
    assert 42 == SpecialMutable.__special__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_133_multiple_inheritance_mutables( module_qname, class_name ):
    ''' Handle mutable attributes with multiple inheritance. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class First(
        metaclass = class_factory_class, mutables = ( 'shared', 'first' )
    ):
        ''' test first parent '''
        shared = 1
        first = 'a'

    class Second(
        metaclass = class_factory_class, mutables = ( 'shared', 'second' )
    ):
        ''' test second parent '''
        shared = 2
        second = 'b'

    class Child( First, Second, mutables = ( 'child', ) ):
        ''' test child '''
        child = 'c'
        fixed = 'd'

    # All declared mutables should work
    Child.shared = 3
    assert 3 == Child.shared
    Child.first = 'changed_a'
    assert 'changed_a' == Child.first
    Child.second = 'changed_b'
    assert 'changed_b' == Child.second
    Child.child = 'changed_c'
    assert 'changed_c' == Child.child
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        Child.fixed = 'attempt'


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_134_mutable_deletion( module_qname, class_name ):
    ''' Handle deletion of mutable attributes. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )

    class DeletableMutable(
        metaclass = class_factory_class,
        mutables = ( 'deletable', 'not_yet_set' )
    ):
        ''' test mutable deletion '''
        deletable = 'original'
        fixed = 'constant'

    # Can delete mutable attribute that exists
    del DeletableMutable.deletable
    assert not hasattr( DeletableMutable, 'deletable' )

    # Can set and then delete mutable attribute that didn't exist at creation
    DeletableMutable.not_yet_set = 'temporary'
    assert 'temporary' == DeletableMutable.not_yet_set
    del DeletableMutable.not_yet_set
    assert not hasattr( DeletableMutable, 'not_yet_set' )

    # Cannot delete immutable attribute
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del DeletableMutable.fixed


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_900_docstring_sanity( module_qname, class_name ):
    ''' Class has valid docstring. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    assert hasattr( class_factory_class, '__doc__' )
    assert isinstance( class_factory_class.__doc__, str )
    assert class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_901_docstring_describes_cfc( module_qname, class_name ):
    ''' Class docstring describes class factory class. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'description of class factory class' )
    assert fragment in class_factory_class.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_902_docstring_mentions_immutability( module_qname, class_name ):
    ''' Class docstring mentions immutability. '''
    module = cache_import_module( module_qname )
    class_factory_class = getattr( module, class_name )
    fragment = base.generate_docstring( 'class attributes immutability' )
    assert fragment in class_factory_class.__doc__
