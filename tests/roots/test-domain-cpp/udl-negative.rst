Invalid user-defined literal suffixes
=====================================

.. cpp:var:: constexpr auto bad_mixed = 1.0f_qs

.. cpp:var:: constexpr auto bad_order = 1llu_qs

.. cpp:var:: constexpr auto bad_digit_suffix = 1e-34q1

.. cpp:var:: constexpr auto bad_symbol = 8_invalid*

.. note::

   Literals with digit-prefixed suffixes such as ``1e-34_1q`` are valid and
   covered by the positive tests; omitting the underscore as in ``1e-34q1`` is
   invalid.

.. cpp:var:: constexpr auto bad_ws = 1 ud
