Fix reflected dictionary union order. ``other | dictionary`` now keeps
``other``'s entries first. Previously ``__ror__`` delegated to
``__or__`` and reversed that order.
