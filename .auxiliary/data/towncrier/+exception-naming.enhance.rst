Exceptions: Rename exception classes for better consistency.

``EntryValidityError`` is now ``EntryInvalidity`` and
``EntryImmutabilityError`` is now ``EntryImmutability``. This is a breaking
change - the old exception names are no longer available.
