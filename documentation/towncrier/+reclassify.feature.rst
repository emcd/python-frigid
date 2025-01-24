⚠️  BREAKING CHANGES! ⚠️  Improve ``reclassify_modules`` to constrain
reclassification to only package modules and not other modules outside of
package. Alter interface to make recursion through subpackages optional. Accept
module objects and module names in addition to module attributes dictionaries.
Attributes dictionaries must contain ``__package__`` or ``__name__`` attribute
now.
