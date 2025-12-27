Invalid user-defined literal suffixes
=====================================

.. cpp:var:: constexpr auto bad_mixed = 1.0f_qs

.. cpp:var:: constexpr auto bad_order = 1llu_qs

.. cpp:var:: constexpr auto bad_digit_start = 1e-34_1q

.. note::

   ``1e-34q1`` is a standards-compliant user-defined literal; the variant with
   ``_1`` exercises the digit-start failure captured by the parser guard.

.. cpp:var:: constexpr auto bad_ws = 1 ud
