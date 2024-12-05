Add ``@immutable`` decorator for making instances of existing classes immutable
after initialization. Compatible with most classes except those defining their
own ``__setattr__`` or ``__delattr__`` methods.
