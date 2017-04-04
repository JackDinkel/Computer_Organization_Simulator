# A few functions to retrieve certain bits from a 32 bit number

#TODO: Are there signed vs unsigned issues?
def Get_Bits_31_26(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0xFC000000
  return (number & mask) >> 26

def Get_Bits_25_21(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x03E00000
  return (number & mask) >> 21

def Get_Bits_20_16(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x001F0000
  return (number & mask) >> 16

def Get_Bits_15_11(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x0000F800
  return (number & mask) >> 11

def Get_Bits_10_6(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x000007C0
  return (number & mask) >> 6

def Get_Bits_5_0(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x0000002F
  return (number & mask)

def Get_Bits_15_0(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x0000FFFF
  return (number & mask)

def Get_Bits_25_0(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF
  mask = 0x03FFFFFF
  return (number & mask)
