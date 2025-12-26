"""
    sphinx.ext.napoleon
    ~~~~~~~~~~~~~~~~~~~

    Support for NumPy and Google style docstrings.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import importlib
import inspect
import sys
from types import ModuleType
from typing import Any, Dict, List, Optional, Sequence

from sphinx import __display_version__ as __version__
from sphinx.application import Sphinx
from sphinx.ext.napoleon.docstring import GoogleDocstring, NumpyDocstring


class Config:
    """Sphinx napoleon extension settings in `conf.py`.

    Listed below are all the settings used by napoleon and their default
    values. These settings can be changed in the Sphinx `conf.py` file. Make
    sure that "sphinx.ext.napoleon" is enabled in `conf.py`::

        # conf.py

        # Add any Sphinx extension module names here, as strings
        extensions = ['sphinx.ext.napoleon']

        # Napoleon settings
        napoleon_google_docstring = True
        napoleon_numpy_docstring = True
        napoleon_include_init_with_doc = False
        napoleon_include_private_with_doc = False
        napoleon_include_special_with_doc = False
        napoleon_use_admonition_for_examples = False
        napoleon_use_admonition_for_notes = False
        napoleon_use_admonition_for_references = False
        napoleon_use_ivar = False
        napoleon_use_param = True
        napoleon_use_rtype = True
        napoleon_use_keyword = True
        napoleon_custom_sections = None

    .. _Google style:
       https://google.github.io/styleguide/pyguide.html
    .. _NumPy style:
       https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

    Attributes
    ----------
    napoleon_google_docstring : :obj:`bool` (Defaults to True)
        True to parse `Google style`_ docstrings. False to disable support
        for Google style docstrings.
    napoleon_numpy_docstring : :obj:`bool` (Defaults to True)
        True to parse `NumPy style`_ docstrings. False to disable support
        for NumPy style docstrings.
    napoleon_include_init_with_doc : :obj:`bool` (Defaults to False)
        True to list ``__init___`` docstrings separately from the class
        docstring. False to fall back to Sphinx's default behavior, which
        considers the ``__init___`` docstring as part of the class
        documentation.

        **If True**::

            def __init__(self):
                \"\"\"
                This will be included in the docs because it has a docstring
                \"\"\"

            def __init__(self):
                # This will NOT be included in the docs

    napoleon_include_private_with_doc : :obj:`bool` (Defaults to False)
        True to include private members (like ``_membername``) with docstrings
        in the documentation. False to fall back to Sphinx's default behavior.

        **If True**::

            def _included(self):
                \"\"\"
                This will be included in the docs because it has a docstring
                \"\"\"
                pass

            def _skipped(self):
                # This will NOT be included in the docs
                pass

    napoleon_include_special_with_doc : :obj:`bool` (Defaults to False)
        True to include special members (like ``__membername__``) with
        docstrings in the documentation. False to fall back to Sphinx's
        default behavior.

        **If True**::

            def __str__(self):
                \"\"\"
                This will be included in the docs because it has a docstring
                \"\"\"
                return unicode(self).encode('utf-8')

            def __unicode__(self):
                # This will NOT be included in the docs
                return unicode(self.__class__.__name__)

    napoleon_use_admonition_for_examples : :obj:`bool` (Defaults to False)
        True to use the ``.. admonition::`` directive for the **Example** and
        **Examples** sections. False to use the ``.. rubric::`` directive
        instead. One may look better than the other depending on what HTML
        theme is used.

        This `NumPy style`_ snippet will be converted as follows::

            Example
            -------
            This is just a quick example

        **If True**::

            .. admonition:: Example

               This is just a quick example

        **If False**::

            .. rubric:: Example

            This is just a quick example

    napoleon_use_admonition_for_notes : :obj:`bool` (Defaults to False)
        True to use the ``.. admonition::`` directive for **Notes** sections.
        False to use the ``.. rubric::`` directive instead.

        Note
        ----
        The singular **Note** section will always be converted to a
        ``.. note::`` directive.

        See Also
        --------
        :attr:`napoleon_use_admonition_for_examples`

    napoleon_use_admonition_for_references : :obj:`bool` (Defaults to False)
        True to use the ``.. admonition::`` directive for **References**
        sections. False to use the ``.. rubric::`` directive instead.

        See Also
        --------
        :attr:`napoleon_use_admonition_for_examples`

    napoleon_use_ivar : :obj:`bool` (Defaults to False)
        True to use the ``:ivar:`` role for instance variables. False to use
        the ``.. attribute::`` directive instead.

        This `NumPy style`_ snippet will be converted as follows::

            Attributes
            ----------
            attr1 : int
                Description of `attr1`

        **If True**::

            :ivar attr1: Description of `attr1`
            :vartype attr1: int

        **If False**::

            .. attribute:: attr1

               Description of `attr1`

               :type: int

    napoleon_use_param : :obj:`bool` (Defaults to True)
        True to use a ``:param:`` role for each function parameter. False to
        use a single ``:parameters:`` role for all the parameters.

        This `NumPy style`_ snippet will be converted as follows::

            Parameters
            ----------
            arg1 : str
                Description of `arg1`
            arg2 : int, optional
                Description of `arg2`, defaults to 0

        **If True**::

            :param arg1: Description of `arg1`
            :type arg1: str
            :param arg2: Description of `arg2`, defaults to 0
            :type arg2: int, optional

        **If False**::

            :parameters: * **arg1** (*str*) --
                           Description of `arg1`
                         * **arg2** (*int, optional*) --
                           Description of `arg2`, defaults to 0

    napoleon_use_keyword : :obj:`bool` (Defaults to True)
        True to use a ``:keyword:`` role for each function keyword argument.
        False to use a single ``:keyword arguments:`` role for all the
        keywords.

        This behaves similarly to  :attr:`napoleon_use_param`. Note unlike
        docutils, ``:keyword:`` and ``:param:`` will not be treated the same
        way - there will be a separate "Keyword Arguments" section, rendered
        in the same fashion as "Parameters" section (type links created if
        possible)

        See Also
        --------
        :attr:`napoleon_use_param`

    napoleon_use_rtype : :obj:`bool` (Defaults to True)
        True to use the ``:rtype:`` role for the return type. False to output
        the return type inline with the description.

        This `NumPy style`_ snippet will be converted as follows::

            Returns
            -------
            bool
                True if successful, False otherwise

        **If True**::

            :returns: True if successful, False otherwise
            :rtype: bool

        **If False**::

            :returns: *bool* -- True if successful, False otherwise

    napoleon_custom_sections : :obj:`list` (Defaults to None)
        Add a list of custom sections to include, expanding the list of parsed sections.

        The entries can either be strings or tuples, depending on the intention:
          * To create a custom "generic" section, just pass a string.
          * To create an alias for an existing section, pass a tuple containing the
            alias name and the original, in that order.

        If an entry is just a string, it is interpreted as a header for a generic
        section. If the entry is a tuple/list/indexed container, the first entry
        is the name of the section, the second is the section key to emulate.


    """
    _config_values = {
        'napoleon_google_docstring': (True, 'env'),
        'napoleon_numpy_docstring': (True, 'env'),
        'napoleon_include_init_with_doc': (False, 'env'),
        'napoleon_include_private_with_doc': (False, 'env'),
        'napoleon_include_special_with_doc': (False, 'env'),
        'napoleon_use_admonition_for_examples': (False, 'env'),
        'napoleon_use_admonition_for_notes': (False, 'env'),
        'napoleon_use_admonition_for_references': (False, 'env'),
        'napoleon_use_ivar': (False, 'env'),
        'napoleon_use_param': (True, 'env'),
        'napoleon_use_rtype': (True, 'env'),
        'napoleon_use_keyword': (True, 'env'),
        'napoleon_custom_sections': (None, 'env')
    }

    def __init__(self, **settings: Any) -> None:
        for name, (default, rebuild) in self._config_values.items():
            setattr(self, name, default)
        for name, value in settings.items():
            setattr(self, name, value)


def setup(app: Sphinx) -> Dict[str, Any]:
    """Sphinx extension setup function.

    When the extension is loaded, Sphinx imports this module and executes
    the ``setup()`` function, which in turn notifies Sphinx of everything
    the extension offers.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Application object representing the Sphinx process

    See Also
    --------
    `The Sphinx documentation on Extensions
    <http://sphinx-doc.org/extensions.html>`_

    `The Extension Tutorial <http://sphinx-doc.org/extdev/tutorial.html>`_

    `The Extension API <http://sphinx-doc.org/extdev/appapi.html>`_

    """
    if not isinstance(app, Sphinx):
        # probably called by tests
        return {'version': __version__, 'parallel_read_safe': True}

    _patch_python_domain()

    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-docstring', _process_docstring)
    app.connect('autodoc-skip-member', _skip_member)

    for name, (default, rebuild) in Config._config_values.items():
        app.add_config_value(name, default, rebuild)
    return {'version': __version__, 'parallel_read_safe': True}


def _patch_python_domain() -> None:
    try:
        from sphinx.domains.python import PyTypedField
    except ImportError:
        pass
    else:
        import sphinx.domains.python
        from sphinx.locale import _
        for doc_field in sphinx.domains.python.PyObject.doc_field_types:
            if doc_field.name == 'parameter':
                doc_field.names = ('param', 'parameter', 'arg', 'argument')
                break
        sphinx.domains.python.PyObject.doc_field_types.append(
            PyTypedField('keyword', label=_('Keyword Arguments'),
                         names=('keyword', 'kwarg', 'kwparam'),
                         typerolename='obj', typenames=('paramtype', 'kwtype'),
                         can_collapse=True))


def _process_docstring(app: Sphinx, what: str, name: str, obj: Any,
                       options: Any, lines: List[str]) -> None:
    """Process the docstring for a given python object.

    Called when autodoc has read and processed a docstring. `lines` is a list
    of docstring lines that `_process_docstring` modifies in place to change
    what Sphinx outputs.

    The following settings in conf.py control what styles of docstrings will
    be parsed:

    * ``napoleon_google_docstring`` -- parse Google style docstrings
    * ``napoleon_numpy_docstring`` -- parse NumPy style docstrings

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Application object representing the Sphinx process.
    what : str
        A string specifying the type of the object to which the docstring
        belongs. Valid values: "module", "class", "exception", "function",
        "method", "attribute".
    name : str
        The fully qualified name of the object.
    obj : module, class, exception, function, method, or attribute
        The object to which the docstring belongs.
    options : sphinx.ext.autodoc.Options
        The options given to the directive: an object with attributes
        inherited_members, undoc_members, show_inheritance and noindex that
        are True if the flag option of same name was given to the auto
        directive.
    lines : list of str
        The lines of the docstring, see above.

        .. note:: `lines` is modified *in place*

    """
    result_lines = lines
    docstring = None  # type: GoogleDocstring
    if app.config.napoleon_numpy_docstring:
        docstring = NumpyDocstring(result_lines, app.config, app, what, name,
                                   obj, options)
        result_lines = docstring.lines()
    if app.config.napoleon_google_docstring:
        docstring = GoogleDocstring(result_lines, app.config, app, what, name,
                                    obj, options)
        result_lines = docstring.lines()
    lines[:] = result_lines[:]


def _unwrap_callable(obj: Any) -> Any:
    try:
        return inspect.unwrap(obj)  # type: ignore[arg-type]
    except (AttributeError, TypeError, ValueError):
        return obj


def _load_module(module_name: Optional[str]) -> Optional[ModuleType]:
    if not module_name:
        return None
    module = sys.modules.get(module_name)
    if module is not None:
        return module
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


def _normalized_qualname_parts(qualname: Optional[str]) -> Sequence[str]:
    if not qualname:
        return ()
    return tuple(part for part in qualname.split('.') if part and part != '<locals>')


def _callable_matches(actual: Any, target: Any) -> bool:
    actual_func = getattr(actual, '__func__', actual)
    target_func = getattr(target, '__func__', target)
    return _unwrap_callable(actual_func) is _unwrap_callable(target_func)


def _owner_paths(parts: Sequence[str], member_name: str) -> Sequence[Sequence[str]]:
    paths: List[Sequence[str]] = []
    if member_name in parts:
        idx = len(parts) - 1 - parts[::-1].index(member_name)
        owner = tuple(parts[:idx])
        if owner:
            paths.append(owner)
    if len(parts) > 1:
        owner = tuple(parts[:-1])
        if owner and owner not in paths:
            paths.append(owner)
    return paths


def _resolve_owner_from_module(module: Optional[ModuleType], candidate: Any,
                               member_name: str) -> Optional[type]:
    if module is None:
        return None
    parts = _normalized_qualname_parts(getattr(candidate, '__qualname__', None))
    if not parts:
        return None
    for owner_path in _owner_paths(parts, member_name):
        current = module
        try:
            for segment in owner_path:
                current = getattr(current, segment)
        except AttributeError:
            continue
        if inspect.isclass(current):
            declared = current.__dict__.get(member_name)
            if declared is not None and _callable_matches(declared, candidate):
                return current
    return None


def _scan_module_for_owner(module: Optional[ModuleType], candidate: Any,
                           member_name: str) -> Optional[type]:
    if module is None:
        return None
    for attr in module.__dict__.values():
        if inspect.isclass(attr):
            declared = attr.__dict__.get(member_name)
            if declared is not None and _callable_matches(declared, candidate):
                return attr
    return None


def _closure_functions(obj: Any) -> Sequence[Any]:
    closure = getattr(obj, '__closure__', None)
    if not closure:
        return ()

    funcs: List[Any] = []
    for cell in closure:
        try:
            value = cell.cell_contents
        except ValueError:
            continue
        if callable(value):
            funcs.append(value)
    return tuple(funcs)


def _resolve_member_owner(obj: Any, member_name: str) -> Optional[type]:
    candidates: List[Any] = []
    seen: List[Any] = []

    def enqueue(candidate: Any) -> None:
        if candidate in seen:
            return
        seen.append(candidate)
        candidates.append(candidate)

    primary = _unwrap_callable(obj)
    enqueue(obj)
    enqueue(primary)
    for func in _closure_functions(obj):
        enqueue(func)
        enqueue(_unwrap_callable(func))

    modules: List[ModuleType] = []
    for candidate in candidates:
        module = _load_module(getattr(candidate, '__module__', None))
        if module and module not in modules:
            modules.append(module)
        owner = _resolve_owner_from_module(module, candidate, member_name)
        if owner is not None:
            return owner

    owner = getattr(obj, '__objclass__', None)
    if inspect.isclass(owner) and member_name in owner.__dict__:
        declared = owner.__dict__.get(member_name)
        if declared is not None and _callable_matches(declared, obj):
            return owner

    for module in modules:
        owner = _scan_module_for_owner(module, obj, member_name)
        if owner is not None:
            return owner

    return None


def _skip_member(app: Sphinx, what: str, name: str, obj: Any,
                 skip: bool, options: Any) -> bool:
    """Determine if private and special class members are included in docs.

    The following settings in conf.py determine if private and special class
    members or init methods are included in the generated documentation:

    * ``napoleon_include_init_with_doc`` --
      include init methods if they have docstrings
    * ``napoleon_include_private_with_doc`` --
      include private members if they have docstrings
    * ``napoleon_include_special_with_doc`` --
      include special members if they have docstrings

    Parameters
    ----------
    app : sphinx.application.Sphinx
        Application object representing the Sphinx process
    what : str
        A string specifying the type of the object to which the member
        belongs. Valid values: "module", "class", "exception", "function",
        "method", "attribute".
    name : str
        The name of the member.
    obj : module, class, exception, function, method, or attribute.
        For example, if the member is the __init__ method of class A, then
        `obj` will be `A.__init__`.
    skip : bool
        A boolean indicating if autodoc will skip this member if `_skip_member`
        does not override the decision
    options : sphinx.ext.autodoc.Options
        The options given to the directive: an object with attributes
        inherited_members, undoc_members, show_inheritance and noindex that
        are True if the flag option of same name was given to the auto
        directive.

    Returns
    -------
    bool
        True if the member should be skipped during creation of the docs,
        False if it should be included in the docs.

    """
    has_doc = getattr(obj, '__doc__', False)
    is_member = (what == 'class' or what == 'exception' or what == 'module')
    if name != '__weakref__' and has_doc and is_member:
        cls_is_owner = False
        if what == 'class' or what == 'exception':
            cls_is_owner = _resolve_member_owner(obj, name) is not None

        if what == 'module' or cls_is_owner:
            is_init = (name == '__init__')
            is_special = (not is_init and name.startswith('__') and
                          name.endswith('__'))
            is_private = (not is_init and not is_special and
                          name.startswith('_'))
            inc_init = app.config.napoleon_include_init_with_doc
            inc_special = app.config.napoleon_include_special_with_doc
            inc_private = app.config.napoleon_include_private_with_doc
            if ((is_special and inc_special) or
                    (is_private and inc_private) or
                    (is_init and inc_init)):
                return False
    return None
