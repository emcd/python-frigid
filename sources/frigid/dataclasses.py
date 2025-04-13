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


# TODO: Once foundational ImmutableClass supports mutables,
#       then enable dynamic docstring generation on classes.


''' Immutable dataclasses. '''


from __future__ import annotations

from . import __
from . import classes as _classes
from . import objects as _objects


_docstring_fragments_core = (
    'description of class factory class',
    'class attributes immutability',
    'dataclass production',
)

doctab: __.DocstringFragmentsTable = __.types.MappingProxyType( {

    'dataclass production': '''
Produces class which is decorated by :py:func:`dataclasses.dataclass`.

Dataclass has ``kw_only`` active to allow inheritance.
Dataclass has ``slots`` active for additional safety and performance.
''',

    'instance attributes immutability': '''
Prevents assignment or deletion of instance attributes after instance creation.
''',

    **_classes.doctab,

} )


_with_docstring = __.funct.partial(
    __.with_docstring, doctab, *_docstring_fragments_core )


@__.typx.dataclass_transform( kw_only_default = True )
class Dataclass(
    type,
    # metaclass = __.ImmutableClass,
    # decorators = ( _with_docstring( ), )
):
    ''' Metaclass which produces immutable dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ Dataclass ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
        **args: __.typx.Any
    ) -> Dataclass:
        class_ = super( ).__new__( clscls, name, bases, namespace, **args )
        decorators_ = ( *decorators, _objects.dataclass_core )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables,
            surveyor = surveyor )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        _classes.class__delattr__(
            selfclass, super( ).__delattr__, name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        _classes.class__setattr__(
            selfclass, super( ).__setattr__, name, value )

    def __dir__( selfclass ) -> __.cabc.Iterable[ str ]:
        return _classes.class__dir__( selfclass, super( ).__dir__ )


@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class DataclassI(
    type,
    # metaclass = __.ImmutableClass,
    # decorators = ( _with_docstring( 'instance attributes immutability' ), ),
):
    ''' Metaclass which produces immutable dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ DataclassI ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
        # TODO? Instance mutables.
        **args: __.typx.Any
    ) -> DataclassI:
        class_ = super( ).__new__( clscls, name, bases, namespace, **args )
        decorators_ = ( *decorators, _objects.immutable_dataclass )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables,
            surveyor = surveyor )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        _classes.class__delattr__(
            selfclass, super( ).__delattr__, name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        _classes.class__setattr__(
            selfclass, super( ).__setattr__, name, value )

    def __dir__( selfclass ) -> __.cabc.Iterable[ str ]:
        return _classes.class__dir__( selfclass, super( ).__dir__ )


@__.typx.dataclass_transform( kw_only_default = True )
class ProtocolDataclass(
    type( __.typx.Protocol ),
    # metaclass = __.ImmutableClass,
    # decorators = ( _with_docstring( ), ),
):
    ''' Metaclass which produces immutable protocol dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ ProtocolDataclass ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
        **args: __.typx.Any
    ) -> ProtocolDataclass:
        class_ = super( ).__new__( clscls, name, bases, namespace, **args )
        decorators_ = ( *decorators, _objects.dataclass_core )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables,
            surveyor = surveyor )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        _classes.class__delattr__(
            selfclass, super( ).__delattr__, name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        _classes.class__setattr__(
            selfclass, super( ).__setattr__, name, value )

    def __dir__( selfclass ) -> __.cabc.Iterable[ str ]:
        return _classes.class__dir__( selfclass, super( ).__dir__ )


@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class ProtocolDataclassI(
    type( __.typx.Protocol ),
    # metaclass = __.ImmutableClass,
    # decorators = ( _with_docstring( 'instance attributes immutability' ), ),
):
    ''' Metaclass which produces immutable protocol dataclasses. '''

    def __new__( # noqa: PLR0913
        clscls: type[ ProtocolDataclassI ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: _classes.ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
        # TODO? Instance mutables.
        **args: __.typx.Any
    ) -> ProtocolDataclassI:
        class_ = super( ).__new__( clscls, name, bases, namespace, **args )
        decorators_ = ( *decorators, _objects.immutable_dataclass )
        return _classes.class__new__(
            class_,
            decorators = decorators_,
            docstring = docstring,
            mutables = mutables,
            surveyor = surveyor )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        _classes.class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        _classes.class__delattr__(
            selfclass, super( ).__delattr__, name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        _classes.class__setattr__(
            selfclass, super( ).__setattr__, name, value )

    def __dir__( selfclass ) -> __.cabc.Iterable[ str ]:
        return _classes.class__dir__( selfclass, super( ).__dir__ )


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
