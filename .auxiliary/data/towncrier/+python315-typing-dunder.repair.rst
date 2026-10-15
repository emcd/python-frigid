Permit CPython 3.15 typing machinery names on immutable classes. CPython 3.15
``typing`` sets ``__typing_is_deprecated_inherited_runtime_protocol__`` during
class decoration and again in the ``runtime_checkable`` decorator, and the
class-level immutability behavior refused it. The typing and ABC machinery
exemptions are now taken from Classcore rather than maintained locally, so
``_is_runtime_protocol`` and ``__non_callable_proto_members__`` are permitted
as well.
