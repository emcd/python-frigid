Pre-import the internal ``exceptions`` submodule in ``frigid.__`` so
that importing ``frigid.__.exceptions`` after module finalization no
longer emits an ``ImportWarning``.
