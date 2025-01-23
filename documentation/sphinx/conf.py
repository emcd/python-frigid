''' Configuration file for the Sphinx documentation builder.

    This file only contains a selection of the most common options.
    For a full list, see the documentation:
        https://www.sphinx-doc.org/en/master/usage/configuration.html
    Also, see this nice article on Sphinx customization:
        https://jareddillard.com/blog/common-ways-to-customize-sphinx-themes.html
'''

# mypy: ignore-errors
# pylint: disable=consider-using-namedtuple-or-dataclass
# ruff: noqa: E402,F401


def _calculate_copyright_notice( ):
    from datetime import datetime as DateTime
    first_year = 2024
    now_year = DateTime.utcnow( ).year
    if first_year < now_year: year_range = f"{first_year}-{now_year}"
    else: year_range = str( first_year )
    return f"{year_range}, Eric McDonald"


def _import_version( ):
    from importlib import import_module
    from pathlib import Path
    from sys import path
    project_location = Path( __file__ ).parent.parent.parent
    path.insert( 0, str( project_location / 'sources' ) )
    module = import_module( 'frigid' )
    return module.__version__


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'python-frigid'
author = 'Eric McDonald'
copyright = ( # pylint: disable=redefined-builtin
    _calculate_copyright_notice( ) )
release = version = _import_version( )

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
    'sphinx_inline_tabs',
]

templates_path = [ '_templates' ]

exclude_patterns = [ ]

rst_prolog = f'''
.. |project| replace:: {project}
'''

nitpicky = True
nitpick_ignore = [
    # Workaround for https://bugs.python.org/issue11975
    # Found on Stack Overflow (credit to Astropy project):
    #   https://stackoverflow.com/a/30624034
    ( 'py:class', "D[k] if k in D, else d.  d defaults to None." ),
    ( 'py:class', "None.  Remove all items from D." ),
    ( 'py:class', "a set-like object providing a view on D's items" ),
    ( 'py:class', "a set-like object providing a view on D's keys" ),
    ( 'py:class', "an object providing a view on D's values" ),
    ( 'py:class', "functools.partial" ),
    ( 'py:class', "mappingproxy" ),
    ( 'py:class', "module" ),
    ( 'py:class',
      "v, remove specified key and return the corresponding value." ),
    # Type annotation weirdnesses.
    ( 'py:class', "Doc" ),
    ( 'py:class', "NotImplementedType" ),
    ( 'py:class', "absence.objects.AbsentSingleton" ),
    ( 'py:class', "frigid.dictionaries._DictionaryOperations" ),
    ( 'py:class', "frigid.__.dictionaries._H" ),
    ( 'py:class', "frigid.__.dictionaries._V" ),
    ( 'py:class', "frigid.__.dictionaries.Annotated" ),
    ( 'py:class', "frigid.__.imports.Annotated" ),
    ( 'py:class', "frigid.__.imports.C" ),
    ( 'py:class', "frigid.__.imports.H" ),
    ( 'py:class', "frigid.__.imports.V" ),
    ( 'py:class', "collections.abc.Annotated" ),
    ( 'py:class', "typing_extensions._ProtocolMeta" ),
    ( 'py:class', "typing_extensions.Annotated" ),
    ( 'py:class', "typing_extensions.Any" ),
    ( 'py:class', "typing_extensions.Never" ),
    ( 'py:class', "typing_extensions.NoDefault" ),
    ( 'py:class', "typing_extensions.Self" ),
    ( 'py:class', "typing_extensions.TypeIs" ),
    ( 'py:class', "types.Annotated" ),
    ( 'py:class', "types.NoneType" ),
    ( 'py:obj', "frigid.__.dictionaries._H" ),
    ( 'py:obj', "frigid.__.dictionaries._V" ),
    ( 'py:obj', "frigid.__.imports.H" ),
    ( 'py:obj', "frigid.__.imports.V" ),
    ( 'py:class', "typing_extensions.Any" ),
]

# -- Options for linkcheck builder -------------------------------------------

linkcheck_ignore = [
    # Circular dependency between building HTML and publishing it.
    r'https://emcd\.github\.io/python-frigid/.*',
    # Stack Overflow rate limits too aggressively, which breaks matrix builds.
    r'https://stackoverflow\.com/help/.*',
    # Repository does not exist during initial development.
    r'https://github\.com/emcd/python-frigid',
    r'https://github\.com/emcd/python-frigid/.*',
    # Package does not exist during initial development.
    r'https://pypi.org/project/frigid/',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.
# https://github.com/pradyunsg/furo
html_theme = 'furo'
html_theme_options = {
    'navigation_with_keys': True,
    'sidebar_hide_name': True,
}

html_static_path = [ '_static' ]

# -- Options for autodoc extension -------------------------------------------

autodoc_default_options = {
    'member-order': 'groupwise',
    'imported-members': False,
    'inherited-members': True,
    'show-inheritance': True,
    'undoc-members': True,
}

#autodoc_typehints = 'description'

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': (
        'https://docs.python.org/3', None),
    'typing-extensions': (
        'https://typing-extensions.readthedocs.io/en/latest', None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
