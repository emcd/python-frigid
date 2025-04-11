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


''' Immutable dataclasses. '''
# TODO: Enhance docstrings specifically for dataclasses.


from __future__ import annotations

from . import __
from . import classes as _classes
from . import objects as _objects


@__.typx.dataclass_transform( kw_only_default = True )
class Dataclass( type ):
    ''' Metaclass which produces immutable dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ Dataclass ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> Dataclass:
        class_ = super( ).__new__( clscls, name, bases, namespace, **args )
        decorators_ = (
            *decorators, __.dcls.dataclass( kw_only = True, slots = True ) )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _classes.class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _classes.class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

Dataclass.__doc__ = __.generate_docstring(
    Dataclass,
    'description of class factory class',
    'class attributes immutability',
    'dataclass production' )


@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class DataclassI( type ):
    ''' Metaclass which produces immutable dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ DataclassI ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        # TODO? Instance mutables.
        **args: __.typx.Any
    ) -> DataclassI:
        class_ = super( ).__new__( clscls, name, bases, namespace, **args )
        decorators_ = ( *decorators, _objects.immutable_dataclass )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _classes.class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _classes.class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

DataclassI.__doc__ = __.generate_docstring(
    DataclassI,
    'description of class factory class',
    'class attributes immutability',
    'dataclass production' )


@__.typx.dataclass_transform( kw_only_default = True )
class ProtocolDataclass( type( __.typx.Protocol ) ):
    ''' Metaclass which produces immutable protocol dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ ProtocolDataclass ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> ProtocolDataclass:
        class_ = super( ProtocolDataclass, clscls ).__new__(
            clscls, name, bases, namespace, **args )
        decorators_ = (
            *decorators, __.dcls.dataclass( kw_only = True, slots = True ) )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _classes.class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _classes.class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ProtocolDataclass.__doc__ = __.generate_docstring(
    ProtocolDataclass,
    'description of class factory class',
    'class attributes immutability',
    'dataclass production' )


@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class ProtocolDataclassI( type( __.typx.Protocol ) ):
    ''' Metaclass which produces immutable protocol dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ ProtocolDataclassI ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        # TODO? Instance mutables.
        **args: __.typx.Any
    ) -> ProtocolDataclassI:
        class_ = super( ProtocolDataclassI, clscls ).__new__(
            clscls, name, bases, namespace, **args )
        decorators_ = ( *decorators, _objects.immutable_dataclass )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not _classes.class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not _classes.class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ProtocolDataclassI.__doc__ = __.generate_docstring(
    ProtocolDataclassI,
    'description of class factory class',
    'class attributes immutability',
    'dataclass production' )


## Deprecated Classes


@__.typx.deprecated( 'Replaced by DataclassI.' )
class CompleteDataclass( DataclassI ): pass

CompleteDataclass.__doc__ = __.generate_docstring(
    CompleteDataclass,
    'description of class factory class',
    'class attributes immutability',
    'dataclass production' )


@__.typx.deprecated( 'Replaced by ProtocolDataclassI.' )
class CompleteProtocolDataclass( ProtocolDataclassI ): pass

CompleteProtocolDataclass.__doc__ = __.generate_docstring(
    CompleteProtocolDataclass,
    'description of class factory class',
    'class attributes immutability',
    'dataclass production' )
