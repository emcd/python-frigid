from dataclasses import dataclass

from typing_extensions import Protocol, dataclass_transform, runtime_checkable

from frigid import ProtocolClass, one

standard_dataclass = dataclass( frozen = True, kw_only = True, slots = True )

@dataclass_transform( )
class Interface(
    Protocol,
    metaclass = ProtocolClass,
    decorators = ( standard_dataclass, runtime_checkable ),
    mutables = one( '__dataclass_transform__' ),
):

    foo: int
    bar: str
    baz: str = ''


@dataclass_transform( )
class Implementation(
    Interface,
    decorators = one( standard_dataclass ),
    mutables = one( '__dataclass_transform__' ),
): pass


i = Implementation( foo = 1, bar = 'x' ) # type: ignore
