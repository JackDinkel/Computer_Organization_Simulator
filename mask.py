from globals import *

####### Decode Helpers ###########################################################
def Get_Bits_31_26(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0xFC000000
  return (number & mask) >> 26

def Get_Bits_25_21(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x03E00000
  return (number & mask) >> 21

def Get_Bits_20_16(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x001F0000
  return (number & mask) >> 16

def Get_Bits_15_11(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x0000F800
  return (number & mask) >> 11

def Get_Bits_10_6(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x000007C0
  return (number & mask) >> 6

def Get_Bits_5_0(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x0000002F
  return (number & mask)

def Get_Bits_15_0(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x0000FFFF
  return (number & mask)

def Get_Bits_25_0(number):
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  mask = 0x03FFFFFF
  return (number & mask)

##################################################################################



###### Byte, Half, and Word masking ##############################################

def Offset_Mask(offset, bits):
  # Generate a mask for a number of bits, right shifted by offset bytes
  mask = (2**bits - 1) << (32 - bits)
  for _ in xrange(offset):
    mask = logical_rshift(mask, 8)
  return mask


def Get_Bits(number, offset, num_bits):
  # Get num_bits bits from a word, offsets count from the left
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  assert offset >= 0   and offset <= 3, "offset out of range: %s" % offset
  assert num_bits >= 0 and num_bits < 32, "num_bits out of range: %s" % num_bits
  return logical_rshift( number & Offset_Mask(offset, num_bits), 32 - num_bits  - (offset * 8) )


def Get_Reverse_Bits(number, offset, num_bits):
  # Get everything except num_bits bits from a word, offsets count from the left
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  assert offset >= 0   and offset <= 3, "offset out of range: %s" % offset
  assert num_bits >= 0 and num_bits < 32, "num_bits out of range: %s" % num_bits
  return number & ~Offset_Mask(offset, num_bits)


def Get_Byte(number, offset):
  # Get a byte from a word, offsets count from the left
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  assert offset >= 0   and offset <= 3, "offset out of range: %s" % offset
  return Get_Bits(number, offset, 8)


def Insert_Byte(original, byte, offset):
  # Insert a byte into an existing number
  assert original >= 0x0 and original <= 0xFFFFFFFF, "original out of range: %s" % original
  assert offset >= 0   and offset <= 3, "offset out of range: %s" % offset
  assert byte >= 0x0 and byte <= 0xFF, "byte out of range: %s" % byte

  return Get_Reverse_Bits(original, offset, 8) | ( byte << 32 - 8 - (offset * 8) )


def Insert_Half(original, half, offset):
  # Insert a half into an existing number
  assert original >= 0x0 and original <= 0xFFFFFFFF, "original out of range: %s" % original
  assert offset == 0 or offset == 2, "offset out of range: %s" % offset
  assert half >= 0x0 and half <= 0xFFFF, "half out of range: %s" % half

  return Get_Reverse_Bits(original, offset, 16) | ( half << 32 - 16 - (offset * 8) )


def Get_Half(number, offset):
  # Get a half word from a word, offsets count from the left
  assert number >= 0x0 and number <= 0xFFFFFFFF, "input out of range: %s" % number
  assert offset == 0 or offset == 2, "offset out of range: %s" % offset
  return Get_Bits(number, offset, 16)


def Generate_Right_Mask(num_bits):
  # Generate a mask with the right num_bits bits set to 1 and everything else zero
  assert num_bits >= 0 and num_bits < 32, "num_bits out of range: %s" % num_bits
  if num_bits == 0:
    return 0
  mask = 1
  for _ in xrange(num_bits-1):
    mask = mask << 1 | mask
  return mask


def Cat_Half(b1, b0):
  # Combine 2 bytes into a half
  assert b0 >= 0x0 and b0 <= 0xff
  assert b1 >= 0x0 and b1 <= 0xff
  
  return (b1 << 8) | b0


def Split_Half(word):
  # Split a half into 2 bytes
  assert word >= 0x0 and word <= 0xffff

  b0 = Get_Byte(word, 0)
  b1 = Get_Byte(word, 1)

  return (b1, b0)


def Cat_Word(b3, b2, b1, b0):
  # Combine 4 bytes into a word
  assert b0 >= 0x0 and b0 <= 0xff
  assert b1 >= 0x0 and b1 <= 0xff
  assert b2 >= 0x0 and b2 <= 0xff
  assert b3 >= 0x0 and b3 <= 0xff

  return (b3 << 24) | (b2 << 16) | (b1 << 8) | b0


def Split_Word(word):
  # Split a word into 4 bytes
  assert word >= 0x0 and word <= 0xffffffff

  b0 = Get_Byte(word, 0)
  b1 = Get_Byte(word, 1)
  b2 = Get_Byte(word, 2)
  b3 = Get_Byte(word, 3)

  return (b3, b2, b1, b0)

##################################################################################