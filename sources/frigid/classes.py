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


''' Immutable classes.

    Provides metaclasses for creating classes with immutable attributes. Once a
    class is initialized, new attributes may not be assigned to it and its
    existing attributes cannot be reassigned or deleted.

    The implementation includes:

    * ``Class``: Standard metaclass for immutable classes; derived from
      :py:class:`type`.
    * ``ABCFactory``: Metaclass for abstract base classes; derived from
      :py:class:`abc.ABCMeta`.
    * ``ProtocolClass``: Metaclass for protocol classes; derived from
      :py:class:`typing.Protocol`.

    Additionally, metaclasses for dataclasses are provided as a convenience.

    >>> from frigid import Class
    >>> class Example( metaclass = Class ):
    ...     x = 1
    >>> Example.y = 2  # Attempt assignment
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'y'.
    >>> Example.x = 3  # Attempt reassignment
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.
''' # noqa: E501

# TODO? Allow predicate functions and regex patterns as mutability checkers.


from __future__ import annotations

from . import __


ClassDecorator: __.typx.TypeAlias = __.cabc.Callable[ [ type ], type ]
ClassDecorators: __.typx.TypeAlias = __.cabc.Sequence[ ClassDecorator ]
ClassDecoratorTp: __.typx.TypeAlias = (
    __.cabc.Callable[ [ type[ __.C ] ], type[ __.C ] ] )
ClassDecoratorsTp: __.typx.TypeAlias = (
    __.cabc.Sequence[ ClassDecoratorTp[ __.C ] ] )


_behavior = 'immutability'


class Class( type ):
    ''' Metaclass which produces immutable classes. '''

    def __new__( # noqa: PLR0913
        clscls: type[ Class ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> Class:
        class_ = type.__new__( clscls, name, bases, namespace, **args )
        return class__new__(
            class_,
            decorators = decorators,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

Class.__doc__ = __.generate_docstring(
    Class,
    'description of class factory class',
    'class attributes immutability' )


class ABCFactory( __.abc.ABCMeta ):
    ''' Metaclass which produces immutable abstract base classes. '''

    def __new__( # noqa: PLR0913
        clscls: type[ ABCFactory ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> ABCFactory:
        class_ = __.abc.ABCMeta.__new__(
            clscls, name, bases, namespace, **args )
        return class__new__(
            class_, decorators = decorators,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ABCFactory.__doc__ = __.generate_docstring(
    ABCFactory,
    'description of class factory class',
    'class attributes immutability' )


class ProtocolClass( type( __.typx.Protocol ) ):
    ''' Metaclass which produces immutable protocol classes. '''

    def __new__( # noqa: PLR0913
        clscls: type[ ProtocolClass ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: ClassDecorators = ( ),
        docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
        mutables: __.cabc.Collection[ str ] = ( ),
        **args: __.typx.Any
    ) -> ProtocolClass:
        class_ = super( ProtocolClass, clscls ).__new__(
            clscls, name, bases, namespace, **args )
        return class__new__(
            class_,
            decorators = decorators,
            docstring = docstring,
            mutables = mutables )

    def __init__( selfclass, *posargs: __.typx.Any, **nomargs: __.typx.Any ):
        super( ).__init__( *posargs, **nomargs )
        class__init__( selfclass )

    def __delattr__( selfclass, name: str ) -> None:
        if not class__delattr__( selfclass, name ):
            super( ).__delattr__( name )

    def __setattr__( selfclass, name: str, value: __.typx.Any ) -> None:
        if not class__setattr__( selfclass, name ):
            super( ).__setattr__( name, value )

ProtocolClass.__doc__ = __.generate_docstring(
    ProtocolClass,
    'description of class factory class',
    'class attributes immutability' )


def class__new__(
    original: type, *,
    decorators: ClassDecorators = ( ),
    docstring: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
    mutables: __.cabc.Collection[ str ] = ( ),
) -> type:
    # Some decorators create new classes, which invokes this method again.
    # Short-circuit to prevent recursive decoration and other tangles.
    class_decorators_ = original.__dict__.get( '_class_decorators_', [ ] )
    if class_decorators_: return original
    if not __.is_absent( docstring ): original.__doc__ = docstring
    original._class_mutables_ = _accumulate_mutables( original, mutables )
    original._class_decorators_ = class_decorators_
    reproduction = original
    for decorator in decorators:
        class_decorators_.append( decorator )
        reproduction = decorator( original )
        if original is not reproduction:
            __.repair_class_reproduction( original, reproduction )
        original = reproduction
    class_decorators_.clear( )  # Flag '__init__' to enable immutability
    return reproduction


def class__init__( class_: type ) -> None:
    # Some metaclasses add class attributes in '__init__' method.
    # So, we wait until last possible moment to set immutability.
    # Consult class attributes dictionary to ignore immutable base classes.
    cdict = class_.__dict__
    if cdict.get( '_class_decorators_' ): return
    del class_._class_decorators_
    if ( class_behaviors := cdict.get( '_class_behaviors_' ) ):
        class_behaviors.add( _behavior )
    else: class_._class_behaviors_ = { _behavior }


def class__delattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    cdict = class_.__dict__
    if name in cdict.get( '_class_mutables_', ( ) ): return False
    if _behavior not in cdict.get( '_class_behaviors_', ( ) ): return False
    from .exceptions import AttributeImmutabilityError
    raise AttributeImmutabilityError( name )


def class__setattr__( class_: type, name: str ) -> bool:
    # Consult class attributes dictionary to ignore immutable base classes.
    cdict = class_.__dict__
    if name in cdict.get( '_class_mutables_', ( ) ): return False
    if _behavior not in cdict.get( '_class_behaviors_', ( ) ): return False
    from .exceptions import AttributeImmutabilityError
    raise AttributeImmutabilityError( name )


def _accumulate_mutables(
    class_: type, mutables: __.cabc.Collection[ str ]
) -> frozenset[ str ]:
    return frozenset( mutables ).union( *(
        frozenset( base.__dict__.get( '_class_mutables_', ( ) ) )
        for base in class_.__mro__ ) )
