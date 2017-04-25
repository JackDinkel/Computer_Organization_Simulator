def logical_rshift(num, shamt):
  return num >> shamt if num >= 0 else (num + 0x100000000) >> shamt
