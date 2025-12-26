Python domain docfields with unions
===================================

.. py:function:: sample(text, choice, nested, maybe, literal, literal_spaced)

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
   :param literal_spaced: literal containing a pipe
   :type literal_spaced: Literal['foo| bar']

.. py:attribute:: sample_attribute

   :vartype sample_attribute: bytes | str
