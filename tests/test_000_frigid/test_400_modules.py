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


''' Assert correct function of modules. '''

# mypy: ignore-errors
# pylint: disable=attribute-defined-outside-init
# pylint: disable=invalid-name,magic-value-comparison,protected-access


import pytest

from itertools import product

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.modules' ) )
THESE_CLASSES_NAMES = ( 'Module', )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates with name. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    obj = Module( 'foo' )
    assert isinstance( obj, Module )
    assert 'foo' == obj.__name__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_immutability( module_qname, class_name ):
    ''' Module prevents attribute modification. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    obj = Module( 'foo' )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        obj.__name__ = 'bar'
    assert 'foo' == obj.__name__
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        del obj.__name__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_500_module_reclassification_by_dict( module_qname, class_name ):
    ''' Modules are correctly reclassified as immutable from dictionary. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType
    m1 = ModuleType( f"{PACKAGE_NAME}.test1" )
    m2 = ModuleType( f"{PACKAGE_NAME}.test2" )
    m3 = ModuleType( "other.module" )
    attrs = {
        '__package__': PACKAGE_NAME,
        'module1': m1,
        'module2': m2,
        'external': m3,
        'other': 42,
    }
    assert not isinstance( m1, Module )
    assert not isinstance( m2, Module )
    assert not isinstance( m3, Module )
    module.reclassify_modules( attrs )
    assert isinstance( m1, Module )
    assert isinstance( m2, Module )
    assert not isinstance( m3, Module )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        m1.new_attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        m2.new_attr = 42
    m3.new_attr = 42  # Should work


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_501_module_reclassification_by_name( module_qname, class_name ):
    ''' Modules are correctly reclassified as immutable from name. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType
    from sys import modules
    test_module = ModuleType( f"{PACKAGE_NAME}.test" )
    test_module.__package__ = PACKAGE_NAME
    modules[ test_module.__name__ ] = test_module
    assert not isinstance( test_module, Module )
    module.reclassify_modules( test_module.__name__ )
    assert isinstance( test_module, Module )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        test_module.new_attr = 42
    modules.pop( test_module.__name__ )  # Cleanup


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_502_module_reclassification_by_object( module_qname, class_name ):
    ''' Modules are correctly reclassified as immutable from object. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType
    test_module = ModuleType( f"{PACKAGE_NAME}.test" )
    test_module.__package__ = PACKAGE_NAME
    assert not isinstance( test_module, Module )
    module.reclassify_modules( test_module )
    assert isinstance( test_module, Module )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        test_module.new_attr = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_503_recursive_module_reclassification( module_qname, class_name ):
    ''' Recursive module reclassification works correctly. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType
    root = ModuleType( f"{PACKAGE_NAME}.test" )
    root.__package__ = PACKAGE_NAME
    sub1 = ModuleType( f"{PACKAGE_NAME}.test.sub1" )
    sub2 = ModuleType( f"{PACKAGE_NAME}.test.sub2" )
    root.sub1 = sub1
    root.sub2 = sub2
    assert not isinstance( root, Module )
    assert not isinstance( sub1, Module )
    assert not isinstance( sub2, Module )
    module.reclassify_modules( root, recursive = True )
    assert isinstance( root, Module )
    assert isinstance( sub1, Module )
    assert isinstance( sub2, Module )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        root.new_attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        sub1.new_attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        sub2.new_attr = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_504_module_reclassification_respects_package(
    module_qname, class_name
):
    ''' Module reclassification only affects package modules. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType
    root = ModuleType( f"{PACKAGE_NAME}.test" )
    root.__package__ = PACKAGE_NAME
    external = ModuleType( "other_package.module" )
    root.external = external
    assert not isinstance( root, Module )
    assert not isinstance( external, Module )
    module.reclassify_modules( root )
    assert isinstance( root, Module )
    assert not isinstance( external, Module )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        root.new_attr = 42
    external.new_attr = 42  # Should work
    assert 42 == external.new_attr


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_505_module_reclassification_requires_package(
    module_qname, class_name
):
    ''' Module reclassification requires package name. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType
    m1 = ModuleType( f"{PACKAGE_NAME}.test1" )
    attrs = { 'module1': m1 }  # Missing __package__ or __name__
    assert not isinstance( m1, Module )
    module.reclassify_modules( attrs )
    assert not isinstance( m1, Module )
    m1.new_attr = 42  # Should work
    assert 42 == m1.new_attr


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
def test_901_docstring_describes_module( module_qname, class_name ):
    ''' Class docstring describes module. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'description of module' )
    assert fragment in Object.__doc__


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_902_docstring_mentions_immutability( module_qname, class_name ):
    ''' Class docstring mentions immutability. '''
    module = cache_import_module( module_qname )
    Object = getattr( module, class_name )
    fragment = base.generate_docstring( 'module attributes immutability' )
    assert fragment in Object.__doc__
