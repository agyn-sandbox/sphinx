"""Tests for ``sphinx.util.docfields`` helpers."""

from types import SimpleNamespace

from docutils import nodes
from docutils.utils import new_document

from sphinx.util.docfields import DocFieldTransformer, TypedField


class _DummyDirective:
    def __init__(self, typed_field: TypedField) -> None:
        self.domain = 'py'
        self.doc_field_types = (typed_field,)
        document = new_document('dummy')
        document.settings.env = None
        self.state = SimpleNamespace(document=document)
        self._typemap = self._build_type_map(typed_field)

    def _build_type_map(self, field: TypedField):
        typemap = {}
        names = field.names or (field.name,)
        for name in names:
            typemap[name] = (field, False)
        for name in field.typenames:
            typemap[name] = (field, True)
        return typemap

    def get_field_type_map(self):
        return self._typemap


def _transform(fields):
    typed_field = TypedField('parameter', names=('param',), typenames=('type',),
                             label='Parameters')
    directive = _DummyDirective(typed_field)
    transformer = DocFieldTransformer(directive)

    field_list = nodes.field_list()
    for kind, argument, body in fields:
        name_text = kind if not argument else f'{kind} {argument}'
        field_name = nodes.field_name('', name_text)
        paragraph = nodes.paragraph('', '', nodes.Text(body))
        field_body = nodes.field_body('', paragraph)
        field = nodes.field('', field_name, field_body)
        field_list += field

    container = nodes.section()
    container += field_list
    transformer.transform(field_list)
    return container[0]


def _extract_paragraph_text(field):
    field_body = field[1]
    bullet_list = field_body[0]
    list_item = bullet_list[0]
    paragraph = list_item[0]
    return paragraph.astext()


def test_typed_field_preserves_comma_joined_arguments():
    field_list = _transform([
        ('param', 'x1, x2', 'combined parameters'),
        ('type', 'x1, x2', 'array_like, optional'),
    ])

    assert _extract_paragraph_text(field_list[0]) == (
        'x1, x2 (array_like, optional) -- combined parameters'
    )


def test_param_type_fallback_still_splits_single_argument():
    field_list = _transform([
        ('param', 'int value', 'single parameter'),
    ])

    assert _extract_paragraph_text(field_list[0]) == (
        'value (int) -- single parameter'
    )


def test_param_type_fallback_handles_comma_in_type_spec():
    field_list = _transform([
        ('param', 'tuple[int,int] pair', 'pair parameter'),
    ])

    assert _extract_paragraph_text(field_list[0]) == (
        'pair (tuple[int,int]) -- pair parameter'
    )
