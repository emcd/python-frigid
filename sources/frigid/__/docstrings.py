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


''' Docstring utilities. '''


from __future__ import annotations

from . import imports as __
from . import doctab # TODO: Legacy: Remove.


ClassDecorator: __.typx.TypeAlias = __.cabc.Callable[ [ type ], type ]
DocstringFragment: __.typx.TypeAlias = str |  __.typx.Doc
DocstringFragmentsTable: __.typx.TypeAlias = __.cabc.Mapping[ str, str ]

WithDocstringFragmentsArgument: __.typx.TypeAlias = __.typx.Annotated[
    DocstringFragment,
    __.typx.Doc(
        ''' Fragments from which to produce a docstring.

            If fragment is a string, then it will be used as an index
            into a table of docstring fragments.
            If fragment is a :pep:`727` ``Doc`` object, then the value of its
            ``documentation`` attribute will be incorporated.
        ''' ),
]
WithDocstringPreserveArgument: __.typx.TypeAlias = __.typx.Annotated[
    bool, __.typx.Doc( ''' Preserve extant docstring? ''' )
]
WithDocstringTableArgument: __.typx.TypeAlias = __.typx.Annotated[
    DocstringFragmentsTable,
    __.typx.Doc( ''' Table from which to copy docstring fragments. ''' ),
]


def with_docstring(
    table: WithDocstringTableArgument, /,
    *fragments: WithDocstringFragmentsArgument,
    # TODO: Injection format for attributes: Suppress | SphinxRst | SphinxMyst
    preserve: WithDocstringPreserveArgument = True,
) -> ClassDecorator:
    # TODO: Generalize to callable objects.
    #       Make override type signature for class decorators.
    ''' Produces docstring from fragments and decorates class with it. '''
    def decorate( cls: type[ __.C ] ) -> type[ __.C ]:
        fragments_: list[ str ] = [ ]
        if preserve:
            fragment = __.inspect.getdoc( cls )
            if fragment: fragments_.append( fragment )
        fragments_.extend(
            (   fragment.documentation
                if isinstance( fragment, __.typx.Doc )
                else table[ fragment ] )
            for fragment in fragments )
        # TODO: Introspect class attributes for documentation.
        docstring = '\n\n'.join(
            __.inspect.cleandoc( fragment ) for fragment in fragments_ )
        cls.__doc__ = docstring if docstring else None
        return cls

    return decorate


class Docstring( str ):
    # TODO: Legacy: Remove.
    ''' Dedicated docstring container. '''


def generate_docstring(
    *fragment_ids: Docstring | str | type,
    table: __.cabc.Mapping[ str, str ] = doctab.TABLE,
) -> str:
    ''' Sews together docstring fragments into clean docstring. '''
    # TODO: Legacy: Remove.
    fragments: list[ str ] = [ ]
    for fragment_id in fragment_ids:
        if __.inspect.isclass( fragment_id ):
            fragment = __.inspect.getdoc( fragment_id ) or ''
        elif isinstance( fragment_id, Docstring ): fragment = fragment_id
        else: fragment = table[ fragment_id ]
        fragments.append( __.inspect.cleandoc( fragment ) )
    return '\n\n'.join( fragments )
