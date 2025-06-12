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


''' Immutable classes. '''


from . import __


is_public_identifier = __.is_public_identifier


def _provide_error_class( name: str ) -> type[ Exception ]:
    ''' Provides error class for this package. '''
    match name:
        case 'AttributeImmutability':
            from .exceptions import AttributeImmutability as error
        case _:
            from .exceptions import ErrorProvideFailure
            raise ErrorProvideFailure( name, reason = 'Does not exist.' )
    return error


_dataclass_core = __.dcls.dataclass( kw_only = True, slots = True )
_dynadoc_configuration = (
    __.ccstd.dynadoc.produce_dynadoc_configuration(
        introspection = __.dynadoc_introspection_control_on_class,
        table = __.fragments ) )
_class_factory = __.funct.partial(
    __.ccstd.class_factory,
    attributes_namer = __.calculate_attrname,
    dynadoc_configuration = _dynadoc_configuration,
    error_class_provider = _provide_error_class )


mutables_default = ( )
visibles_default = ( is_public_identifier, )


@_class_factory( )
class Class( type ):
    ''' Metaclass for standard classes. '''

    _dynadoc_fragments_ = (
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class Dataclass( type ):
    ''' Metaclass for standard dataclasses. '''

    _dynadoc_fragments_ = (
        'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( kw_only_default = True )
class DataclassMutable( type ):
    ''' Metaclass for dataclasses with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
class AbstractBaseClass( __.abc.ABCMeta ):
    ''' Metaclass for standard abstract base classes. '''

    _dynadoc_fragments_ = (
        'cfc produce abstract base class',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
class ProtocolClass( type( __.typx.Protocol ) ):
    ''' Metaclass for standard protocol classes. '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( frozen_default = True, kw_only_default = True )
class ProtocolDataclass( type( __.typx.Protocol ) ):
    ''' Metaclass for standard protocol dataclasses. '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class', 'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal', 'cfc instance protect' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


@_class_factory( )
@__.typx.dataclass_transform( kw_only_default = True )
class ProtocolDataclassMutable( type( __.typx.Protocol ) ):
    ''' Metaclass for protocol dataclasses with mutable instance attributes.
    '''

    _dynadoc_fragments_ = (
        'cfc produce protocol class', 'cfc produce dataclass',
        'cfc class conceal', 'cfc class protect', 'cfc dynadoc',
        'cfc instance conceal' )

    def __new__( # Typechecker stub.
        clscls: type[ __.T ],
        name: str,
        bases: tuple[ type, ... ],
        namespace: dict[ str, __.typx.Any ], *,
        decorators: __.ClassDecorators[ __.T ] = ( ),
        **arguments: __.typx.Unpack[ __.ccstd.ClassFactoryExtraArguments ],
    ) -> __.T:
        return super( ).__new__( clscls, name, bases, namespace )


class Object( metaclass = Class ):
    ''' Standard base class. '''

    _dynadoc_fragments_ = (
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance protect' )


class ObjectMutable( metaclass = Class, instances_mutables = '*' ):
    ''' Base class with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


class DataclassObject( metaclass = Dataclass ):
    ''' Standard base dataclass. '''

    _dynadoc_fragments_ = (
        'dataclass',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance protect' )


class DataclassObjectMutable( metaclass = DataclassMutable ):
    ''' Base dataclass with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'dataclass',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


class Protocol( __.typx.Protocol, metaclass = ProtocolClass ):
    ''' Standard base protocol class. '''

    _dynadoc_fragments_ = (
        'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance protect' )


class ProtocolMutable(
    __.typx.Protocol, metaclass = ProtocolClass, instances_mutables = '*'
):
    ''' Base protocol class with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


class DataclassProtocol(
    __.typx.Protocol, metaclass = ProtocolDataclass,
):
    ''' Standard base protocol dataclass. '''

    _dynadoc_fragments_ = (
        'dataclass', 'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal', 'class instance protect' )


class DataclassProtocolMutable(
    __.typx.Protocol, metaclass = ProtocolDataclassMutable,
):
    ''' Base protocol dataclass with mutable instance attributes. '''

    _dynadoc_fragments_ = (
        'dataclass', 'protocol class',
        'class concealment', 'class protection', 'class dynadoc',
        'class instance conceal' )


dataclass_with_standard_behaviors = (
    __.funct.partial(
        __.ccstd.dataclass_with_standard_behaviors,
        attributes_namer = __.calculate_attrname,
        error_class_provider = _provide_error_class ) )


with_standard_behaviors = (
    __.funct.partial(
        __.ccstd.with_standard_behaviors,
        attributes_namer = __.calculate_attrname,
        error_class_provider = _provide_error_class ) )
