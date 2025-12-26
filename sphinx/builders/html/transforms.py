"""
    sphinx.builders.html.transforms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Transforms for HTML builder.

    :copyright: Copyright 2007-2020 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from docutils import nodes

from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.nodes import NodeMatcher


class KeyboardTransform(SphinxPostTransform):
    """Transform :kbd: role to more detailed form.

    Before::

        <literal class="kbd">
            Control-x

    After::

        <literal class="kbd">
            <literal class="kbd">
                Control
            -
            <literal class="kbd">
                x
    """
    default_priority = 400
    builders = ('html',)
    pattern = re.compile(r'(?<=\S)(?:-|\+|\^|\s+)(?=\S)')

    def run(self, **kwargs: Any) -> None:
        matcher = NodeMatcher(nodes.literal, classes=["kbd"])
        for node in self.document.traverse(matcher):  # type: nodes.literal
            masked_text, placeholders = self._mask_escaped_separators(
                node.astext(), getattr(node, 'rawsource', None))
            parts = self.pattern.split(masked_text)
            if len(parts) == 1:
                continue

            separators = self.pattern.findall(masked_text)

            node[:] = []
            for index, key in enumerate(parts):
                restored_key = self._restore_placeholders(key, placeholders)
                node += nodes.literal('', restored_key, classes=["kbd"])

                if index < len(separators):
                    separator = self._restore_placeholders(separators[index], placeholders)
                    node += nodes.Text(separator)

    def _mask_escaped_separators(self, text: str, rawsource: Optional[str]) -> Tuple[str, Dict[str, str]]:
        placeholders: Dict[str, str] = {}
        escaped_indices = self._find_escaped_indices(text, rawsource)
        if not escaped_indices:
            return text, placeholders

        masked_parts: List[str] = []
        for index, char in enumerate(text):
            if index in escaped_indices and char in '-+^':
                placeholder = f'@KBD_ESC_{len(placeholders)}@'
                placeholders[placeholder] = char
                masked_parts.append(placeholder)
            else:
                masked_parts.append(char)

        return ''.join(masked_parts), placeholders

    def _find_escaped_indices(self, text: str, rawsource: Optional[str]) -> Set[int]:
        if not rawsource:
            return set()

        start = rawsource.find('`')
        end = rawsource.rfind('`')
        if start == -1 or end <= start:
            content = rawsource
        else:
            content = rawsource[start + 1:end]

        indices: Set[int] = set()
        text_index = 0
        pos = 0
        text_len = len(text)

        while pos < len(content) and text_index < text_len:
            char = content[pos]
            if char == '\\':
                if pos + 1 >= len(content):
                    pos += 1
                    continue

                escaped = content[pos + 1]
                if escaped in '-+^':
                    indices.add(text_index)

                pos += 2
                text_index += 1
                continue

            pos += 1
            text_index += 1

        return indices

    @staticmethod
    def _restore_placeholders(text: str, placeholders: Dict[str, str]) -> str:
        for placeholder, char in placeholders.items():
            text = text.replace(placeholder, char)
        return text


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_post_transform(KeyboardTransform)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
