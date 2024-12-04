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
def test_500_module_reclassification( module_qname, class_name ):
    ''' Modules are correctly reclassified as immutable. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType as Module_
    m1 = Module_( 'm1' )
    m2 = Module_( 'm2' )
    m3 = Module( 'm3' )
    attrs = { 'bar': 42, 'orb': True, 'm1': m1, 'm2': m2, 'm3': m3 }
    assert not isinstance( m1, Module )
    assert not isinstance( m2, Module )
    assert isinstance( m3, Module )
    module.reclassify_modules( attrs )
    assert isinstance( m1, Module )
    assert isinstance( m2, Module )
    assert isinstance( m3, Module )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        m1.new_attr = 42
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        m2.new_attr = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_501_module_reclassification_with_custom_type(
    module_qname, class_name
):
    ''' Modules can be reclassified to custom module type. '''
    module = cache_import_module( module_qname )
    Module = getattr( module, class_name )
    from types import ModuleType as Module_

    class CustomModule( Module ):
        ''' foo '''

    m1 = Module_( 'm1' )
    attrs = { 'm1': m1 }
    module.reclassify_modules( attrs, to_class = CustomModule )
    assert isinstance( m1, CustomModule )
    with pytest.raises( exceptions.AttributeImmutabilityError ):
        m1.new_attr = 42


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
