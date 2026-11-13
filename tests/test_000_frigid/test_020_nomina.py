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


''' Assert correct function of nomina utilities. '''


import pytest

from .__ import PACKAGE_NAME, cache_import_module


@pytest.mark.parametrize( 'name,expected', [
    ( 'public_name', True ),
    ( 'another_public', True ),
    ( 'CamelCase', True ),
    ( 'snake_case', True ),
    ( 'single', True ),
    ( '_private_name', False ),
    ( '__dunder__', False ),
    ( '__private', False ),
    ( '_', False ),
    ( '__class__', False ),
])
def test_100_is_public_identifier( name, expected ):
    ''' Function correctly identifies public identifiers. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    assert module.is_public_identifier( name ) is expected


_LEVELS = ( 'class', 'classes', 'instance', 'instances' )
_CORES = (
    'behaviors',
    'construction_arguments',
    'dynadoc_configuration',
    'in_progress',
    'mutables_names', 'mutables_predicates', 'mutables_regexes',
    'visibles_names', 'visibles_predicates', 'visibles_regexes',
    'assigner_core', 'deleter_core', 'surveyor_core' )
# The two class-level mangling stems. Generation emits these bare; only their
# completed 64-hex digest forms are internal. Never assert
# 'is_internal_name( namer( level, core ) )' universally.
_MANGLED_STEMS = ( ( 'class', 'behaviors' ), ( 'class', 'in_progress' ) )


def _detected( namer, name ):
    ''' Detects a generated name without relying on private vocabulary. '''
    return namer.is_internal_name( name ) or namer.is_internal_name(
        name + 'a' * 64 )


def test_200_calculate_attrname_shape( ):
    ''' Namer is the shared calculator configured for this package. '''
    from classcore.standard.nomina import AttrnameCalculator
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    assert isinstance( module.calculate_attrname, AttrnameCalculator )
    assert module.calculate_attrname.package_name == module.package_name
    assert (
        module.calculate_attrname( 'class', 'behaviors' )
        == f"_{module.package_name}_class_behaviors_" )


def test_201_calculate_attrname_detects_generated_names( ):
    ''' Every generated name is detected. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    namer = module.calculate_attrname
    for level in _LEVELS:
        for core in _CORES:
            assert _detected( namer, namer( level, core ) )


def test_202_calculate_attrname_rejects_lookalikes( ):
    ''' Grammar lookalikes are rejected. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    namer = module.calculate_attrname
    for name in (
        f"_{module.package_name}_custom_",
        f"_{module.package_name}_class_custom_",
        f"_{module.package_name}_",
        'custom_name',
        '_classcore_class_mutables_names_',
    ):
        assert not _detected( namer, name )


@pytest.mark.parametrize( 'level,core', _MANGLED_STEMS )
def test_203_calculate_attrname_mangled_asymmetry( level, core ):
    ''' Bare mangling stems are not internal; completed digest forms are. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    namer = module.calculate_attrname
    stem = namer( level, core )
    assert not namer.is_internal_name( stem )
    assert namer.is_internal_name( stem + 'a' * 64 )
    assert not namer.is_internal_name( stem + 'a' * 63 )
    assert not namer.is_internal_name( stem + 'z' * 64 )


@pytest.mark.parametrize( 'level', _LEVELS )
@pytest.mark.parametrize( 'core', _CORES )
def test_204_calculate_attrname_static_stems_detectable( level, core ):
    ''' Non-mangling stems are detected in their generated form. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    namer = module.calculate_attrname
    if ( level, core ) in _MANGLED_STEMS: return
    assert namer.is_internal_name( namer( level, core ) )


def test_205_calculate_attrname_prefix_is_read_only( ):
    ''' The configured prefix cannot drift after construction. '''
    module = cache_import_module( f"{PACKAGE_NAME}.__.nomina" )
    namer = module.calculate_attrname
    with pytest.raises( AttributeError ):
        namer.package_name = 'other'
    assert namer.package_name == module.package_name


def _collect_namer_sites( ):
    ''' Collects (source, referenced name) for every attributes_namer site. '''
    import ast
    from pathlib import Path

    def referenced( value ):
        ''' Name of the attribute or name a value node refers to. '''
        if isinstance( value, ast.Attribute ): return value.attr
        if isinstance( value, ast.Name ): return value.id
        return type( value ).__name__

    def from_defaults( node, sites, path ):
        args = node.args
        pairs = list( zip( args.args[ -len( args.defaults ): ],
                           args.defaults ) )
        pairs += [ ( a, d ) for a, d in
                   zip( args.kwonlyargs, args.kw_defaults ) if d is not None ]
        sites.extend(
            ( path, referenced( default ) )
            for arg, default in pairs if 'attributes_namer' == arg.arg )

    sites = [ ]
    for filepath in Path( 'sources' ).rglob( '*.py' ):
        source = filepath.read_text( )
        path = str( filepath )
        for node in ast.walk( ast.parse( source ) ):
            if isinstance( node, ast.Call ):
                sites.extend(
                    ( path, referenced( keyword.value ) )
                    for keyword in node.keywords
                    if 'attributes_namer' == keyword.arg )
            elif isinstance( node, ( ast.FunctionDef, ast.AsyncFunctionDef ) ):
                from_defaults( node, sites, path )
    return sites


def _collect_namer_definitions( ):
    ''' Collects source paths binding the namer name. '''
    import ast
    from pathlib import Path

    def targets( node ):
        ''' Binding names introduced by a definition node. '''
        if isinstance( node, ( ast.FunctionDef, ast.AsyncFunctionDef ) ):
            return [ node.name ]
        if isinstance( node, ast.Assign ):
            return [ t.id for t in node.targets if isinstance( t, ast.Name ) ]
        if isinstance( node, ast.AnnAssign ):
            target = node.target
            return [ target.id ] if isinstance( target, ast.Name ) else [ ]
        return [ ]

    found = [ ]
    for filepath in Path( 'sources' ).rglob( '*.py' ):
        path = str( filepath )
        nodes = ast.walk( ast.parse( filepath.read_text( ) ) )
        found.extend(
            path for node in nodes
            if 'calculate_attrname' in targets( node ) )
    return found


def test_206_namer_inventory_uses_shared_calculator( ):
    ''' Every namer site in the sources uses the shared calculator.

        Guards against a hand-rolled namer being reintroduced at a call
        site, which would silently stop contributing internal names.
    '''
    sites = _collect_namer_sites( )
    assert sites, 'no attributes_namer sites found; scan is vacuous'
    # A site either names the shared calculator directly or forwards the
    # 'attributes_namer' parameter, whose default the scan also checks.
    for path, name in sites:
        allowed = ( 'calculate_attrname', 'attributes_namer' )
        assert name in allowed, ( path, name )
    assert 5 <= len( sites )


def test_207_namer_defined_in_canonical_module_only( ):
    ''' The namer is bound nowhere outside its canonical module.

        A same-named shadow elsewhere would satisfy the name check in
        test_206 while not being the shared calculator.
    '''
    canonical = 'sources/frigid/__/nomina.py'
    found = _collect_namer_definitions( )
    assert found, 'no calculate_attrname definition found; scan is vacuous'
    for path in found:
        assert canonical == path, path
