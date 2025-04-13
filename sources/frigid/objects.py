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


''' Immutable objects.

    Provides a base class and decorator for creating objects with immutable
    attributes. Once an object is initialized, its attributes cannot be modified
    or deleted.

    >>> from frigid import Object
    >>> class Point( Object ):
    ...     def __init__( self, x, y ):
    ...         self.x = x
    ...         self.y = y
    ...         super( ).__init__( )
    ...
    >>> obj = Point( 1, 2 )  # Initialize with attributes
    >>> obj.z = 3  # Attempt to add attribute
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'z'.
    >>> obj.x = 4  # Attempt modification
    Traceback (most recent call last):
    ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.

    The `immutable` decorator can be used to make any class immutable:

    >>> from frigid import immutable
    >>> @immutable
    ... class Config:
    ...     def __init__( self, verbose = False ):
    ...         self.verbose  = verbose
    ...
    >>> config = Config( verbose = True )
    >>> config.verbose = False  # Attempt to modify attribute
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: ...
''' # noqa: E501


# ruff: noqa: F811


from __future__ import annotations

from . import __
from . import classes as _classes


_behavior = 'immutability'
_behaviors_name = '_behaviors_'
_empty_dictproxy: __.types.MappingProxyType[ str, __.typx.Any ] = (
    __.types.MappingProxyType( { } ) )


DecoratorInitNomargsArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Union[
        __.cabc.Mapping[ str, __.typx.Any ],
        __.cabc.Callable[
            [ type[ __.C ] ], __.cabc.Mapping[ str, __.typx.Any ] ],
    ],
    __.typx.Doc(
        ''' Nominative arguments to inject on ``__init__`` invocation.

            May be either a mapping or a function which produces a mapping.
            If absent, then no nominative arguments are injected.
        ''' ),
]
DecoratorInitPosargsArgument: __.typx.TypeAlias = __.typx.Annotated[
    __.typx.Union[
        __.cabc.Sequence[ __.typx.Any ],
        __.cabc.Callable[
            [ type[ __.C ] ], __.cabc.Sequence[ __.typx.Any ] ],
    ],
    __.typx.Doc(
        ''' Positional arguments to inject on ``__init__`` invocation.

            May be either a sequence or a function which produces a sequence.
            If absent, then no positional arguments are injected.
        ''' ),
]


dataclass_core = __.dcls.dataclass( kw_only = True, slots = True )


@__.typx.overload
def immutable( # noqa: PLR0913 # pragma: no branch
    class_: type[ __.C ], *,
    decorators: _classes.ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    init_nomargs: DecoratorInitNomargsArgument[ __.C ] = _empty_dictproxy,
    init_posargs: DecoratorInitPosargsArgument[ __.C ] = ( ),
    mutables: __.cabc.Collection[ str ] = ( ),
    surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
) -> type[ __.C ]: ...


@__.typx.overload
def immutable( # noqa: PLR0913 # pragma: no branch
    class_: __.AbsentSingleton, *,
    decorators: _classes.ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    init_nomargs: DecoratorInitNomargsArgument[ __.C ] = _empty_dictproxy,
    init_posargs: DecoratorInitPosargsArgument[ __.C ] = ( ),
    mutables: __.cabc.Collection[ str ] = ( ),
    surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
) -> _classes.ClassDecoratorTp[ __.C ]: ...


def immutable( # noqa: PLR0913
    class_: __.Absential[ type[ __.C ] ] = __.absent, *,
    decorators: _classes.ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    init_nomargs: DecoratorInitNomargsArgument[ __.C ] = _empty_dictproxy,
    init_posargs: DecoratorInitPosargsArgument[ __.C ] = ( ),
    mutables: __.cabc.Collection[ str ] = ( ),
    surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
) -> type[ __.C ] | _classes.ClassDecoratorTp[ __.C ]:
    ''' Decorator which makes class instances immutable.

        Immutability is enforced after initialization.

        This decorator can be used in different ways:

        1. Simple decorator:

           >>> from frigid import immutable
           >>> @immutable
           ... class Config:
           ...     pass

        2. With arguments:

           >>> from frigid import immutable
           >>> @immutable( mutables = ( 'version', ) )
           ... class Config:
           ...     pass
    '''
    def decorate( cls: type[ __.C ] ) -> type[ __.C ]:
        cls.__annotations__[ _behaviors_name ] = set[ str ]
        for decorator in decorators:
            cls_ = decorator( cls )
            if cls is cls_: continue
            __.repair_class_reproduction( cls, cls_ )
            cls = cls_
        if not __.is_absent( docstring ): cls.__doc__ = docstring
        _associate_init( cls, init_nomargs, init_posargs )
        if not __.is_absent( surveyor ): _associate_dir( cls, surveyor )
        mutables_ = frozenset( mutables )
        _associate_delattr( cls, mutables_ )
        _associate_setattr( cls, mutables_ )
        return cls

    if not __.is_absent( class_ ): return decorate( class_ )
    return decorate # No class to decorate; keyword arguments only.


@__.typx.overload
def immutable_dataclass( # pragma: no branch
    class_: type[ __.C ], *,
    decorators: _classes.ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    mutables: __.cabc.Collection[ str ] = ( ),
    surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
) -> type[ __.C ]: ...


@__.typx.overload
def immutable_dataclass( # pragma: no branch
    class_: __.AbsentSingleton, *,
    decorators: _classes.ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    mutables: __.cabc.Collection[ str ] = ( ),
    surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
) -> _classes.ClassDecoratorTp[ __.C ]: ...


def immutable_dataclass(
    class_: __.Absential[ type[ __.C ] ] = __.absent, *,
    decorators: _classes.ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    mutables: __.cabc.Collection[ str ] = ( ),
    surveyor: __.Absential[ _classes.AttributesSurveyor ] = __.absent,
) -> type[ __.C ] | _classes.ClassDecoratorTp[ __.C ]:
    ''' Decorator which makes dataclass instances immutable.

        Immutability is enforced after complete initialization.
        Unlike ``dataclasses.dataclass( frozen = True )``, this decorator
        allows for ``__post_init__`` to execute before immutability is
        enforced.

        Dataclass instances are slotted for performance and extra safety.

        Dataclass instances can only be initialized from keyword arguments;
        this allows for dataclass inheritance with indeterminate argument
        order.
    '''
    dcls_decorator = dataclass_core
    dcls_nomargs: dict[ str, __.typx.Any ] = { _behaviors_name: set( ) }
    return immutable(
        class_ = class_,
        decorators = ( *decorators, dcls_decorator ),
        docstring = docstring,
        init_nomargs = dcls_nomargs,
        mutables = mutables,
        surveyor = surveyor )


def _associate_init(
    cls: type[ __.C ],
    init_nomargs: DecoratorInitNomargsArgument[ __.C ],
    init_posargs: DecoratorInitPosargsArgument[ __.C ],
) -> None:
    original_init = getattr( cls, '__init__' )
    init_nomargs_ = (
        init_nomargs( cls ) if callable( init_nomargs ) else init_nomargs )
    init_posargs_ = (
        init_posargs( cls ) if callable( init_posargs ) else init_posargs )

    @__.funct.wraps( original_init )
    def __init__(
        self: object, *posargs: __.typx.Any, **nomargs: __.typx.Any
    ) -> None:
        original_init(
            self,
            *( *init_posargs_, *posargs ),
            **{ **init_nomargs_, **nomargs } )
        behaviors: __.cabc.MutableSet[ str ]
        if _check_dict( self ):
            attributes = getattr( self, '__dict__' )
            behaviors = attributes.get( _behaviors_name, set( ) )
            if not behaviors: attributes[ _behaviors_name ] = behaviors
        else:
            behaviors = getattr( self, _behaviors_name, set( ) )
            if not behaviors: setattr( self, _behaviors_name, behaviors )
        behaviors.add( _behavior )

    cls.__init__ = __init__


def _associate_delattr(
    cls: type[ __.C ], mutables: __.cabc.Collection[ str ]
) -> None:
    original_delattr = getattr( cls, '__delattr__' )

    def __delattr__( self: object, name: str ) -> None:
        if name in mutables:
            original_delattr( self, name )
            return
        if _check_behavior( self ): # pragma: no branch
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        original_delattr( self, name ) # pragma: no cover

    cls.__delattr__ = __delattr__


def _associate_setattr(
    cls: type[ __.C ], mutables: __.cabc.Collection[ str ]
) -> None:
    original_setattr = getattr( cls, '__setattr__' )

    def __setattr__( self: object, name: str, value: __.typx.Any ) -> None:
        if name in mutables:
            original_setattr( self, name, value )
            return
        if _check_behavior( self ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        original_setattr( self, name, value )

    cls.__setattr__ = __setattr__


def _associate_dir(
    cls: type[ __.C ], surveyor: _classes.AttributesSurveyor
) -> None:
    original_dir = getattr( cls, '__dir__' )

    def __dir__( self: object ) -> __.cabc.Iterable[ str ]:
        return surveyor( self, __.funct.partial( original_dir, self ) )

    cls.__dir__ = __dir__


@immutable
class Object:
    ''' Immutable objects. '''

    __slots__ = ( '__dict__', _behaviors_name )

    def __repr__( self ) -> str:
        return "{fqname}( )".format( fqname = __.calculate_fqname( self ) )

Object.__doc__ = __.generate_docstring(
    Object, 'instance attributes immutability' )


def _check_behavior( obj: object ) -> bool:
    behaviors: __.cabc.MutableSet[ str ]
    if _check_dict( obj ):
        attributes = getattr( obj, '__dict__' )
        behaviors = attributes.get( _behaviors_name, set( ) )
    else: behaviors = getattr( obj, _behaviors_name, set( ) )
    return _behavior in behaviors


def _check_dict( obj: object ) -> bool:
    # Return False even if '__dict__' in '__slots__'.
    if hasattr( obj, '__slots__' ): return False
    return hasattr( obj, '__dict__' )
