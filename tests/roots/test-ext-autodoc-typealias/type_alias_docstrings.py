"""Fixtures for type alias docstring handling tests."""

from pathlib import Path
from typing import Any, Callable, Dict, Optional


ScaffoldOpts = Dict[str, Any]
"""Dictionary with PyScaffold's options, see ``pyscaffold.api.create_project``.
Should be treated as immutable (copy before mutating).

Please notice some behaviours given by the options **SHOULD** be observed. For
example, files should be overwritten when the **force** option is ``True``.
Similarly when **pretend** is ``True``, no operation should be really
performed, but any action should be logged as if realized.
"""


FileContents = Optional[str]
"""When the file content is ``None``, the file should not be written to disk.
Empty files are represented by an empty string ``""`` as content.
"""


FileOp = Callable[[Path, FileContents, ScaffoldOpts], Optional[Path]]
"""Signature of functions considered file operations::

    Callable[[Path, FileContents, ScaffoldOpts], Optional[Path]]

- **path** (:class:`pathlib.Path`): file path potentially written to disk.
- **contents** (:obj:`FileContents`): usual text content. :obj:`None` skips
  writing the file.
- **opts** (:obj:`ScaffoldOpts`): a dict with PyScaffold's options.

If a file is written (or permissions are changed) the implementation should
return the :class:`pathlib.Path`. Otherwise :obj:`None` should be returned.
"""
