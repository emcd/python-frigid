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


''' Assert correct function of installers. '''

# pylint: disable=no-member,undefined-variable
# ruff: noqa: F821


from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.installers"


def test_100_install_one_with_default( ):
    ''' Install_one function adds one to builtins by default. '''
    module = cache_import_module( MODULE_QNAME )
    module.install( )
    assert ( 42, ) == one( 42 )
    import builtins
    del builtins.one


def test_101_install_one_with_name( ):
    ''' Install_one function accepts custom name. '''
    module = cache_import_module( MODULE_QNAME )
    module.install( 'single' )
    assert ( 42, ) == single( 42 )
    import builtins
    del builtins.single


def test_102_install_one_skip( ):
    ''' Install_one function accepts None to skip. '''
    module = cache_import_module( MODULE_QNAME )
    module.install( None )
    import builtins
    assert not hasattr( builtins, 'one' )


def test_900_docstring_sanity( ):
    ''' Function has valid docstring. '''
    module = cache_import_module( MODULE_QNAME )
    assert hasattr( module.install, '__doc__' )
    assert isinstance( module.install.__doc__, str )
    assert module.install.__doc__


def test_901_docstring_has_examples( ):
    ''' Function docstring includes examples. '''
    module = cache_import_module( MODULE_QNAME )
    assert 'Example' in module.install.__doc__
