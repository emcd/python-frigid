Align protocol metaclass inheritance with ``classcore``.
``ProtocolDataclass`` now inherits from ``ProtocolClass``, and
``ProtocolDataclassMutable`` inherits from ``ProtocolDataclass``. A
protocol dataclass can now also be a ``ProtocolClass`` protocol without
a metaclass conflict.
