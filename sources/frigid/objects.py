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


# pylint: disable=line-too-long
''' Immutable objects.

    Provides a base class and decorator for creating objects with immutable
    attributes. Once an object is initialized, its attributes cannot be modified
    or deleted.

    The implementation uses a special dictionary type for attribute storage that
    enforces immutability. This makes it suitable for:

    * Configuration objects
    * Value objects
    * Immutable data containers
    * Objects requiring attribute stability

    >>> from frigid import Object
    >>> obj = Object( x = 1, y = 2 )  # Initialize with attributes
    >>> obj.z = 3  # Attempt to add attribute
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'z'.
    >>> obj.x = 4  # Attempt modification
    Traceback (most recent call last):
        ...
    frigid.exceptions.AttributeImmutabilityError: Cannot assign or delete attribute 'x'.
'''
# pylint: enable=line-too-long


from . import __


def immutable( class_: type[ __.C ] ) -> type[ __.C ]:
    ''' Decorator that makes a class immutable after initialization.

        Cannot be applied to classes that define their own __setattr__
        or __delattr__ methods.
    '''
    for method in ( '__setattr__', '__delattr__' ):
        if method in class_.__dict__:
            from .exceptions import DecoratorCompatibilityError
            raise DecoratorCompatibilityError( class_.__name__, method )
    original_init = next(
        base.__dict__[ '__init__' ] for base in class_.__mro__
        if '__init__' in base.__dict__ )

    def __init__(
        self: object, *posargs: __.a.Any, **nomargs: __.a.Any
    ) -> None:
        attributes = super( class_, self ).__getattribute__( '__dict__' )
        #super( class_, self ).__setattr__( '__dict__', { } )
        behaviors: __.cabc.MutableSet[ str ] = (
            attributes.get( '_behaviors_', set( ) ) )
        super( class_, self ).__setattr__( '_behaviors_', behaviors )
        original_init( self, *posargs, **nomargs )
        super( class_, self ).__setattr__(
            '__dict__', __.DictionaryProxy( attributes ) )
        behaviors.add( 'immutability' )

    def __delattr__( self: object, name: str ) -> None:
        if __.behavior_label in getattr( self, '_behaviors_', ( ) ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( class_, self ).__delattr__( name )

    def __setattr__( self: object, name: str, value: __.a.Any ) -> None:
        if __.behavior_label in getattr( self, '_behaviors_', ( ) ):
            from .exceptions import AttributeImmutabilityError
            raise AttributeImmutabilityError( name )
        super( class_, self ).__setattr__( name, value )

    class_.__init__ = __init__
    class_.__delattr__ = __delattr__
    class_.__setattr__ = __setattr__
    return class_


@immutable
class Object:
    ''' Base class for immutable objects.

        Instances become immutable after initialization.
        Attempts to modify attributes after initialization will raise
        AttributeImmutabilityError.
    '''

    __slots__ = ( '__dict__', '_behaviors_' )
