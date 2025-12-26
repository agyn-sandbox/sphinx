Literal nitpicky annotations
=============================

.. py:module:: literal_examples

.. py:class:: SomeEnum

   .. py:attribute:: VALUE

.. py:function:: f(a: Literal[True]) -> Literal["x"]

.. py:function:: g(a: Literal[True, 1, "x", None])

.. py:function:: h(a: Literal[SomeEnum.VALUE])

.. py:function:: j(a: Union[Literal[True], bool])

.. py:function:: k(a: Annotated[Literal["a"], int])

.. py:function:: df(a)

   :type a: Literal["A", "B"]
