def logical_rshift(num, shamt):
  return num >> shamt if num >= 0 else (num + 0x100000000) >> shamt


def twos_comp(val, num_bits):
  # Returns 2's comp interpreted value from unsigned
  if (val > 0):
    if (val & (1 << (num_bits - 1))) != 0:
      val = val - (1 << num_bits)
  return val


def unsigned(val, num_bits):
  # Returns an unsigned representation from a 2's comp value
  return (1 << num_bits) + val if val < 0 else val


def Sign_Extend(input_val, num_bits):
  # Sign extend to 32 bits
  twos_val = twos_comp(input_val, num_bits)
  return twos_val if twos_val >= 0 else (twos_val + 0x100000000)
