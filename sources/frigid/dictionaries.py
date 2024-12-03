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
''' Immutable dictionaries.

    Dictionaries which cannot be modified after creation.

    * :py:class:`AbstractDictionary`:
      Base class defining the immutable dictionary interface. Implementations
      must provide ``__getitem__``, ``__iter__``, and ``__len__``.

    * :py:class:`Dictionary`:
      Standard implementation of an immutable dictionary. Supports all usual
      dict read operations but prevents any modifications.

    * :py:class:`ValidatorDictionary`:
      Validates entries before addition using a supplied predicate function.

    >>> from frigid import Dictionary
    >>> d = Dictionary( x = 1, y = 2 )
    >>> d[ 'z' ] = 3  # Attempt to add entry
    Traceback (most recent call last):
        ...
    frigid.exceptions.EntryImmutabilityError: Cannot assign or delete entry for 'z'.
    >>> d[ 'x' ] = 4  # Attempt modification
    Traceback (most recent call last):
        ...
    frigid.exceptions.EntryImmutabilityError: Cannot assign or delete entry for 'x'.
    >>> del d[ 'y' ]  # Attempt removal
    Traceback (most recent call last):
        ...
    frigid.exceptions.EntryImmutabilityError: Cannot assign or delete entry for 'y'.
'''
# pylint: enable=line-too-long


from . import __
from . import classes as _classes
from . import objects as _objects


class AbstractDictionary( __.cabc.Mapping[ __.H, __.V ] ):
    ''' Abstract base class for immutable dictionaries.

        An immutable dictionary prevents modification or removal of entries
        after creation. This provides a clean interface for dictionaries
        that should never change.

        Implementations must provide:
        - __getitem__, __iter__, __len__
    '''

    @__.abstract_member_function
    def __iter__( self ) -> __.cabc.Iterator[ __.H ]:
        raise NotImplementedError  # pragma: no coverage

    @__.abstract_member_function
    def __len__( self ) -> int:
        raise NotImplementedError  # pragma: no coverage

    @__.abstract_member_function
    def __getitem__( self, key: __.H ) -> __.V:
        raise NotImplementedError  # pragma: no coverage

    def __setitem__( self, key: __.H, value: __.V ) -> None:
        from .exceptions import EntryImmutabilityError
        raise EntryImmutabilityError( key )

    def __delitem__( self, key: __.H ) -> None:
        from .exceptions import EntryImmutabilityError
        raise EntryImmutabilityError( key )


class _DictionaryOperations( AbstractDictionary[ __.H, __.V ] ):
    ''' Mix-in providing additional dictionary operations. '''

    def __init__( self, *posargs: __.a.Any, **nomargs: __.a.Any ) -> None:
        super( ).__init__( *posargs, **nomargs )

    def __or__( self, other: __.cabc.Mapping[ __.H, __.V ] ) -> __.a.Self:
        if not isinstance( other, __.cabc.Mapping ): return NotImplemented
        data = dict( self )
        data.update( other )
        return self.with_data( data )

    def __ror__( self, other: __.cabc.Mapping[ __.H, __.V ] ) -> __.a.Self:
        if not isinstance( other, __.cabc.Mapping ): return NotImplemented
        return self | other

    def __and__(
        self,
        other: __.cabc.Set[ __.H ] | __.cabc.Mapping[ __.H, __.V ]
    ) -> __.a.Self:
        if isinstance( other, __.cabc.Mapping ):
            return self.with_data(
                ( key, value ) for key, value in self.items( )
                if key in other and other[ key ] == value )
        if isinstance( other, ( __.cabc.Set, __.cabc.KeysView ) ):
            return self.with_data(
                ( key, self[ key ] ) for key in self.keys( ) & other )
        return NotImplemented

    def __rand__(
        self,
        other: __.cabc.Set[ __.H ] | __.cabc.Mapping[ __.H, __.V ]
    ) -> __.a.Self:
        if not isinstance(
            other, ( __.cabc.Mapping, __.cabc.Set, __.cabc.KeysView )
        ): return NotImplemented
        return self & other

    @__.abstract_member_function
    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        raise NotImplementedError # pragma: no coverage

    @__.abstract_member_function
    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument[ __.H, __.V ],
        **entries: __.DictionaryNominativeArgument[ __.V ],
    ) -> __.a.Self:
        ''' Creates new dictionary with same behavior but different data. '''
        raise NotImplementedError # pragma: no coverage


class _Dictionary(
    __.ImmutableDictionary[ __.H, __.V ], metaclass = _classes.Class
): pass


class Dictionary( # pylint: disable=eq-without-hash
    _objects.Object, _DictionaryOperations[ __.H, __.V ]
):
    ''' Immutable dictionary. '''

    __slots__ = ( '_data_', )

    _data_: _Dictionary[ __.H, __.V ]

    def __init__(
        self,
        *iterables: __.DictionaryPositionalArgument[ __.H, __.V ],
        **entries: __.DictionaryNominativeArgument[ __.V ],
    ) -> None:
        self._data_ = _Dictionary( *iterables, **entries )
        super( ).__init__( )

    def __iter__( self ) -> __.cabc.Iterator[ __.H ]:
        return iter( self._data_ )

    def __len__( self ) -> int:
        return len( self._data_ )

    def __repr__( self ) -> str:
        return "{fqname}( {contents} )".format(
            fqname = __.calculate_fqname( self ),
            contents = self._data_.__repr__( ) )

    def __str__( self ) -> str:
        return str( self._data_ )

    def __contains__( self, key: __.a.Any ) -> bool:
        return key in self._data_

    def __getitem__( self, key: __.H ) -> __.V:
        return self._data_[ key ]

    def __eq__( self, other: __.a.Any ) -> __.ComparisonResult:
        if isinstance( other, __.cabc.Mapping ):
            return self._data_ == other
        return NotImplemented

    def __ne__( self, other: __.a.Any ) -> __.ComparisonResult:
        if isinstance( other, __.cabc.Mapping ):
            return self._data_ != other
        return NotImplemented

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def get(
        self, key: __.H, default: __.Optional[ __.V ] = __.absent
    ) -> __.a.Annotation[
        __.V,
        __.a.Doc(
            'Value of entry, if it exists. '
            'Else, supplied default value or ``None``.' )
    ]:
        ''' Retrieves entry associated with key, if it exists. '''
        if __.is_absent( default ):
            return self._data_.get( key )  # type: ignore
        return self._data_.get( key, default )

    def keys( self ) -> __.cabc.KeysView[ __.H ]:
        ''' Provides iterable view over dictionary keys. '''
        return self._data_.keys( )

    def items( self ) -> __.cabc.ItemsView[ __.H, __.V ]:
        ''' Provides iterable view over dictionary items. '''
        return self._data_.items( )

    def values( self ) -> __.cabc.ValuesView[ __.V ]:
        ''' Provides iterable view over dictionary values. '''
        return self._data_.values( )

    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument[ __.H, __.V ],
        **entries: __.DictionaryNominativeArgument[ __.V ],
    ) -> __.a.Self:
        return type( self )( *iterables, **entries )

Dictionary.__doc__ = __.generate_docstring(
    Dictionary, 'dictionary entries immutability' )
# Register as subclass of Mapping rather than use it as mixin.
# We directly implement, for the sake of efficiency, the methods which the
# mixin would provide.
__.cabc.Mapping.register( Dictionary )  # type: ignore


class ValidatorDictionary( Dictionary[ __.H, __.V ] ):
    ''' Immutable dictionary with validation of entries on initialization. '''

    __slots__ = ( '_validator_', )

    _validator_: __.DictionaryValidator[ __.H, __.V ]

    def __init__(
        self,
        validator: __.DictionaryValidator[ __.H, __.V ],
        /,
        *iterables: __.DictionaryPositionalArgument[ __.H, __.V ],
        **entries: __.DictionaryNominativeArgument[ __.V ],
    ) -> None:
        self._validator_ = validator
        from itertools import chain
        for key, value in chain.from_iterable( map( # type: ignore
            lambda element: ( # type: ignore
                element.items( )
                if isinstance( element, __.cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ):
            if not self._validator_( key, value ): # type: ignore
                from .exceptions import EntryValidityError
                raise EntryValidityError( key, value )
        super( ).__init__( *iterables, **entries )

    def __repr__( self ) -> str:
        return "{fqname}( {validator}, {contents} )".format(
            fqname = __.calculate_fqname( self ),
            validator = self._validator_.__repr__( ),
            contents = self._data_.__repr__( ) )

    def copy( self ) -> __.a.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self._validator_, self )

    def with_data(
        self,
        *iterables: __.DictionaryPositionalArgument[ __.H, __.V ],
        **entries: __.DictionaryNominativeArgument[ __.V ],
    ) -> __.a.Self:
        ''' Creates new dictionary with same behavior but different data. '''
        return type( self )( self._validator_, *iterables, **entries )

ValidatorDictionary.__doc__ = __.generate_docstring(
    ValidatorDictionary,
    'dictionary entries immutability',
    'dictionary entries validation',
)