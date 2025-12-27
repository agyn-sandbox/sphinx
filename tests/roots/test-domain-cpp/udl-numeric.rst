Numeric user-defined literals
==============================

.. cpp:var:: constexpr auto udl_decimal = 42_km

.. cpp:var:: constexpr auto udl_hex = 0x2A_km

.. cpp:var:: constexpr auto udl_binary = 0b1010_unit

.. cpp:var:: constexpr auto udl_float = 3.14_q_s

.. cpp:var:: constexpr auto hf1 = 0x1.0p+2ud

.. cpp:var:: constexpr auto hf2 = 0x1p2_ud

.. cpp:var:: constexpr auto iu1 = 42f_s

.. cpp:var:: constexpr auto iu2 = 10Funit

.. cpp:namespace:: units::si

.. cpp:var:: inline constexpr auto planck_constant = 6.62607015e-34q_J * 1q_s


Builtin literal suffix regression
---------------------------------

.. cpp:var:: constexpr auto builtin_u = 1u

.. cpp:var:: constexpr auto builtin_U = 1U

.. cpp:var:: constexpr auto builtin_l = 1l

.. cpp:var:: constexpr auto builtin_L = 1L

.. cpp:var:: constexpr auto builtin_f = 1.0f

.. cpp:var:: constexpr auto builtin_F = 1.0F

.. note::

   Digit separator examples such as ``1'000_km`` remain unsupported by the
   test fixtures due to the base literal regular expressions.
