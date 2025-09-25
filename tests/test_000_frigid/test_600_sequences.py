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


''' Assert correct function of sequence utilities. '''


from .__ import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.sequences"


def test_100_one_basic_operation( ):
    ''' One function creates single-item tuples. '''
    module = cache_import_module( MODULE_QNAME )
    assert ( 42, ) == module.one( 42 )
    assert ( None, ) == module.one( None )
    assert ( 'test', ) == module.one( 'test' )
    nested = module.one( module.one( 42 ) )
    assert ( ( 42, ), ) == nested


def test_300_one_with_generator( ):
    ''' One function works in generator expressions. '''
    module = cache_import_module( MODULE_QNAME )
    result = tuple( module.one( x ) for x in range( 3 ) )
    assert ( ( 0, ), ( 1, ), ( 2, ) ) == result


def test_301_one_with_comprehension( ):
    ''' One function works in list comprehensions. '''
    module = cache_import_module( MODULE_QNAME )
    result = [ module.one( x ) for x in range( 3 ) ]
    assert [ ( 0, ), ( 1, ), ( 2, ) ] == result


def test_302_one_with_map( ):
    ''' One function works with map. '''
    module = cache_import_module( MODULE_QNAME )
    result = tuple( map( module.one, range( 3 ) ) )
    assert ( ( 0, ), ( 1, ), ( 2, ) ) == result


def test_900_docstring_sanity( ):
    ''' Function has valid docstring. '''
    module = cache_import_module( MODULE_QNAME )
    assert hasattr( module.one, '__doc__' )
    assert isinstance( module.one.__doc__, str )
    assert module.one.__doc__
