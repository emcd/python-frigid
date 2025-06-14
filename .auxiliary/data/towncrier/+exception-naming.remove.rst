Exceptions: Rename exception classes for better consistency.

* ``AttributeImmutabilityError`` is now ``AttributeImmutability``
* ``EntryImmutabilityError`` is now ``EntryImmutability``
* ``EntryValidityError`` is now ``EntryInvalidity``

This is a breaking change - the old exception names are no longer available.
