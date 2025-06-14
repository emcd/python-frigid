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


''' Assert correct function of namespaces. '''


import pytest

from itertools import product

from . import (
    MODULES_QNAMES,
    PACKAGE_NAME,
    cache_import_module,
)


THESE_MODULE_QNAMES = tuple(
    name for name in MODULES_QNAMES if name.endswith( '.namespaces' ) )
THESE_CLASSES_NAMES = ( 'Namespace', )

base = cache_import_module( f"{PACKAGE_NAME}.__" )
exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_100_instantiation( module_qname, class_name ):
    ''' Class instantiates with various input types. '''
    module = cache_import_module( module_qname )
    Namespace = getattr( module, class_name )
    ns1 = Namespace( )
    assert isinstance( ns1, Namespace )
    ns2 = Namespace(
        ( ( 'foo', 1 ), ( 'bar', 2 ) ), { 'unicorn': True }, orb = False )
    assert isinstance( ns2, Namespace )
    assert 1 == ns2.foo
    assert 2 == ns2.bar
    assert ns2.unicorn
    assert not ns2.orb
    # assert ( 'foo', 'bar', 'unicorn', 'orb' ) == tuple( ns2.__dict__.keys( )
    # assert ( 1, 2, True, False ) == tuple( ns2.__dict__.values( )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_101_immutability( module_qname, class_name ):
    ''' Namespace prevents attribute modification after initialization. '''
    module = cache_import_module( module_qname )
    Namespace = getattr( module, class_name )
    ns1 = Namespace( attr = 42 )
    with pytest.raises( exceptions.AttributeImmutability ):
        ns1.attr = -1
    assert 42 == ns1.attr
    with pytest.raises( exceptions.AttributeImmutability ):
        del ns1.attr
    assert 42 == ns1.attr
    with pytest.raises( exceptions.AttributeImmutability ):
        ns1.new_attr = 'test'
    ns2 = Namespace( )
    with pytest.raises( exceptions.AttributeImmutability ):
        ns2.attr = 42


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_102_string_representation( module_qname, class_name ):
    ''' Namespace has expected string representations. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    ns1 = factory( )
    assert base.ccutils.qualify_class_name( type( ns1 ) ) in repr( ns1 )
    ns2 = factory( a = 1, b = 2 )
    assert base.ccutils.qualify_class_name( type( ns2 ) ) in repr( ns2 )
    assert 'a = 1, b = 2' in repr( ns2 )


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_105_namespace_equality( module_qname, class_name ):
    ''' Namespace compares properly with other namespaces. '''
    from types import SimpleNamespace
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    ns1 = factory( foo = 1, bar = 2 )
    ns2 = factory( foo = 1, bar = 2 )
    assert ns1 == ns2
    assert ns2 == ns1
    ns3 = SimpleNamespace( foo = 1, bar = 2 )
    assert ns1 == ns3
    assert ns3 == ns1
    assert not ( ns1 == -1 ) # noqa: SIM201
    assert ns1 != -1
    assert ns1 != ( )
    ns4 = factory( foo = 1, bar = 3 )
    assert ns1 != ns4
    assert ns4 != ns1


@pytest.mark.parametrize(
    'module_qname, class_name',
    product( THESE_MODULE_QNAMES, THESE_CLASSES_NAMES )
)
def test_106_namespace_initialization_validation( module_qname, class_name ):
    ''' Namespace properly handles various initialization inputs. '''
    module = cache_import_module( module_qname )
    factory = getattr( module, class_name )
    ns1 = factory( { 'a': 1, 'b': 2 } )
    assert 1 == ns1.a
    assert 2 == ns1.b
    ns2 = factory( [ ( 'c', 3 ), ( 'd', 4 ) ] )
    assert 3 == ns2.c
    assert 4 == ns2.d
    ns3 = factory( e = 5, f = 6 )
    assert 5 == ns3.e
    assert 6 == ns3.f
    ns4 = factory( { 'g': 7 }, [ ( 'h', 8 ) ], i = 9 )
    assert 7 == ns4.g
    assert 8 == ns4.h
    assert 9 == ns4.i


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
