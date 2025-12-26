Python domain docfields with unions
===================================

.. py:function:: sample(text, choice, nested, maybe, literal)

   :param text: textual data
   :type text: bytes | str
   :param choice: legacy union syntax
   :type choice: str or int or None
   :param nested: nested generics
   :type nested: dict[str | int, list[None | int]]
   :param maybe: union with ellipsis
   :type maybe: tuple[int, ...] | None
   :param literal: literal pipe
   :type literal: Literal['|']

.. py:attribute:: sample_attribute

   :vartype sample_attribute: bytes | str
