'''
  Conventions and design:
    All hardware constructs are First_Letter_Capitalized_And_Word_Separated_By_Underscore
    All local variables are lower_case_and_word_separated_by_underscore
    All hardware control logic lines are CapitalCamelCase

    Each component of the computer diagrams in the book has a corresponding function or class
    Components that have state are classes
    Components that are combinatorial are functions with inputs and outputs

    The general idea is to emulate hardware, so each function is always called whether or not
    it is actually needed, and multiplexors make the decisions
'''

from control import ALU_DICT
from globals import *
import mask

def twos_comp(val, num_bits):
  # Returns 2's comp interpreted value from unsigned
  if (val > 0):
    if (val & (1 << (num_bits - 1))) != 0:
      val = val - (1 << num_bits)
  return val

def unsigned(val, num_bits):
  # Returns an unsigned representation from a 2's comp value
  return (1 << num_bits) + val if val < 0 else val

##### Hardware ######

## General ##
def MUX(input1, input2, control):
  assert control == 0 or control == 1, "control out of bounds: %s" % control

  if control == 0:
    return input1
  else:
    return input2


class Register(object):
  __value = 0

  def __init__(self):
    self.__value = 0

  def Set(self, new_val):
    assert unsigned(new_val, 32) >= 0x0 and unsigned(new_val, 32) <= 0xFFFFFFFF, "new_val out of bounds: %s" % new_val
    self.__value = new_val

  def Get(self):
    return self.__value


class Memory(object):
  # NOTE: We decided to model this as a combination of word addressable and byte addressable
  # This is a divergence from lec 21, but I leave it here for reference
  # Outside this class, everything is byte addressable, as normal
  # Inside this class, memory is word addressed, so each list element stores a single word
  # Simply divide the address by 4 to get the index, and % by 4 to get the offset

  # A list of all instructions
  __data = []

  #def __init__(self, size):
  #  self.__data = [0 for _ in xrange(size/4)]

  def __init__(self, contents, size):
      self.__data = contents
      for _ in xrange(size - len(self.__data)):
        self.__data.append(0)

  def __del__(self):
    self.__data = []

  def Load_Word(self, address):
    index = address / 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    return self.__data[index]

  def Load_Half(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert offset == 0 or offset == 2, "offset out of bounds: %s" % offset
    word = self.__data[index]
    return Sign_Extend(mask.Get_Half(word, offset), 16)

  def Load_Half_Unsigned(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert offset == 0 or offset == 2, "offset out of bounds: %s" % offset
    word = self.__data[index]
    return mask.Get_Half(word, offset)

  def Load_Byte(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert offset == 0 or offset == 2, "offset out of bounds: %s" % offset
    word = self.__data[index]
    return Sign_Extend(mask.Get_Byte(word, offset), 8)

  def Load_Byte_Unsigned(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    word = self.__data[index]
    return mask.Get_Byte(word, offset)
    
  def Store_Word(self, address, data):
    index = address / 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert unsigned(data, 32) >= 0x0 and unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    self.__data[index] = data

  def Store_Half(self, address, data):
    index = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert unsigned(data, 32) >= 0x0 and unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    assert offset == 0 or offset == 2, "offset out of bounds: %s" % offset

    shamt = offset * 8

    # Get current word
    word = self.Load_Word(address)
    mask = ~(0xFFFF << shamt)
    shifted_word = word & mask

    # Update current word
    shifted_data = data << shamt
    word_to_write = shifted_word | shifted_data

    # Write updated word
    self.__data[index] = word_to_write

  def Store_Byte(self, address, data):
    index = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert unsigned(data, 32) >= 0x0 and unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    assert offset >= 0 and offset < 4

    shamt = offset * 8

    # Get current word
    word = self.Load_Word(address)
    mask = ~(0xFF << shamt)
    shifted_word = word & mask
    print "shifted word", hex(shifted_word)

    # Update current word
    print "data", hex(data)
    shifted_data = data << shamt
    word_to_write = shifted_word | shifted_data
    print "word to write", hex(word_to_write)

    # Write updated word
    self.__data[index] = word_to_write

  def Data_Operate(self, address, write_data, MemRead, MemWrite, Op):
    read_data = 0

    if MemRead:
      assert Op >= 12 and Op <= 16, "Op out of bounds: %s" % Op
      if Op == ALU_DICT["LW"]:
        read_data = Memory.Load_Word(self, address)
      if Op == ALU_DICT["LBU"]:
        read_data = Memory.Load_Byte_Unsigned(self, address)
      if Op == ALU_DICT["LHU"]:
        read_data = Memory.Load_Half_Unsigned(self, address)

    if MemWrite:
      assert Op >= 17 and Op <= 19, "Op out of bounds: %s" % Op
      if Op == ALU_DICT["SB"]:
        Memory.Store_Byte(self, address, write_data)
      if Op == ALU_DICT["SH"]:
        Memory.Store_Half(self, address, write_data)
      if Op == ALU_DICT["SW"]:
        Memory.Store_Word(self, address, write_data)
      if Op == ALU_DICT["SLT"]:
        Memory.Store_Word(self, address, write_data)

    return read_data

  def Instruction_Operate(self, address, write_data, MemRead, MemWrite):
    read_data = 0


    if MemRead:
      read_data = Memory.Load_Word(self, address)
    if MemWrite:
      Memory.Store_Word(self, address, write_data)

    return read_data

  def display(self):
    print self.__data



## Instruction Fetch ##
def PC_Input_Mux(incremented, branch_addr, jump_addr, Branch, Jump):
  # TODO: This needs a closer look, page 271
  mux1 = MUX(incremented, branch_addr, Branch)
  return MUX(mux1, jump_addr, Jump)



class PC(Register):
  pass
  # TODO: Do we need a bunch of addwords if this isn't initialized to 0?
  # TODO: If so, does that need to happen for the memories as well?



#class Instruction_Memory(Memory):
#  def __init__(self, size):
#    Memory.__init__(self, size)



def Add_Four(input_num):
  #TODO: Error bounds
  return input_num + 4 # Only add 1 for Word Address



def Register_Input_Mux(i_type_reg, r_type_reg, RegDst):
  return MUX(i_type_reg, r_type_reg, RegDst)
  


## Instruction Decode and Register File Read ##
class Register_File(object):
  __register_list = []

  def __init__(self):
    # Initialize list of 32 registers
    self.__register_list = [ Register() for _ in range(32) ]

  def GetList(self):
    return [reg.Get() for reg in self.__register_list]

  def Get(self, index):
    assert index >= 0 and index < 32
    return self.__register_list[index].Get()

  def Set(self, index, data):
    assert index >= 0 and index < 32
    return self.__register_list[index].Set(data)

  def Operate(self, read_reg_1, read_reg_2, write_reg, write_data, RegWrite):
    assert read_reg_1 >= 0 and read_reg_1 < 32, "read_reg_1 out of bounds: %d" % read_reg_1
    assert read_reg_2 >= 0 and read_reg_2 < 32, "read_reg_2 out of bounds: %d" % read_reg_2
    assert write_reg  >= 0 and write_reg  < 32, "write_reg out of bounds: %d" % write_reg
    assert unsigned(write_data, 32) >= 0x0 and unsigned(write_data, 32) <= 0xFFFFFFFF, "write_data out of bounds: %s" % write_data
    assert RegWrite == 0 or RegWrite == 1, "RegWrite out of bounds: %s" % RegWrite

    if RegWrite:
      self.__register_list[write_reg].Set(write_data)

    read_data_1 = self.__register_list[read_reg_1].Get()
    read_data_2 = self.__register_list[read_reg_2].Get()

    return read_data_1, read_data_2



def Sign_Extend(input_val, num_bits):
  # Sign extend to 32 bits
  twos_val = twos_comp(input_val, num_bits)
  return twos_val if twos_val >= 0 else (twos_val + 0x100000000)


## Execute and Address Calculation ##
def ALU_Input_Mux1(register1, register2, ALUSrc1):
  return MUX(register1, register2, ALUSrc1)

def ALU_Input_Mux2(register, sign_extended, ALUSrc2):
  return MUX(register, sign_extended, ALUSrc2)



def ALU(input1, input2, shamt, ALUControl):
  # TODO: How does this interface with ALU Control? What is the zero Zero line on page 265?
  if   ALUControl == ALU_DICT["J"]:
    return 0, 1, 0
  elif ALUControl == ALU_DICT["AND"]:
    return input1 & input2, 0, 0
  elif ALUControl == ALU_DICT["OR"]:
    return input1 | input2, 0, 0
  elif ALUControl == ALU_DICT["ADD"]:
    input1 = twos_comp(input1, 32)
    input2 = twos_comp(input2, 32)
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["ADDU"]:
    return unsigned(input1, 32) + unsigned(input2, 32), 0, 0 # TODO
  elif ALUControl == ALU_DICT["SUB"]:
    input1 = twos_comp(input1, 32)
    input2 = twos_comp(input2, 32)
    return input1 - input2, 0, 0
  elif ALUControl == ALU_DICT["SUBU"]:
    return unsigned(input1, 32) - unsigned(input2, 32), 0, 0 # TODO
  elif ALUControl == ALU_DICT["SLL"]:
    return input2 << shamt, 0, 0
  elif ALUControl == ALU_DICT["SRL"]:
    return logical_rshift(input2, shamt), 0, 0
  elif ALUControl == ALU_DICT["SLT"]:
    return ( input1 < input2 ), 0, 1 # TODO
  elif ALUControl == ALU_DICT["SLTU"]:
    return ( unsigned(input1, 32) < unsigned(input2, 32) ), 0, 1 # TODO
  elif ALUControl == ALU_DICT["NOT"]:
    return ~input1, 0, 0
  elif ALUControl == ALU_DICT["LW"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LH"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LB"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LHU"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LBU"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LUI"]:
    return (input2 << 16) | (input1 & 0x0000FFFF), 0, 0
  elif ALUControl == ALU_DICT["SW"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["SH"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["SB"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["NOR"]:
    return ~(input1 | input2), 0, 0
  elif ALUControl == ALU_DICT["MOVZ"]:
    return (input1, 0, 1) if input2 == 0 else (0, 0, 0) # TODO
  elif ALUControl == ALU_DICT["MOVN"]:
    return (input1, 0, 1) if input2 != 0 else (0, 0, 0) # TODO
  elif ALUControl == ALU_DICT["XOR"]:
    return (input1 ^ input2), 0, 0
  elif ALUControl == ALU_DICT["BLTZ"]:
    return (0, 1, 0) if input1 < 0 else (0, 0, 0)
  elif ALUControl == ALU_DICT["BLEZ"]:
    return (0, 1, 0) if input1 <= 0 else (0, 0, 0)
  elif ALUControl == ALU_DICT["BGTZ"]:
    return (0, 1, 0) if input1 > 0 else (0, 0, 0)
  elif ALUControl == ALU_DICT["J"]:
    return 0, 0, 0
  elif ALUControl == ALU_DICT["JAL"]:
    return "pc", 0, 1 # TODO
  elif ALUControl == ALU_DICT["BEQ"]:
    return (0, 0, 1) if input1 == input2 else (0, 0, 0)
  elif ALUControl == ALU_DICT["BNE"]:
    return (0, 0, 1) if input1 != input2 else (0, 0, 0)
  else:
    assert 1 == 2, "Invalid Operation: %s" % ALUControl



def Shift_Left_2(unshifted_num):
  return unshifted_num << 2 # Using Word Addresses



def Calculate_Jump_Addr(unshifted_num, next_pc):
  # This takes the place of the shift left 2 and concatenation components on page 271
  # TODO: assert unshifted_num is in bounds (26 bits)
  mask = 0xF0000000
  pc_upper = next_pc & mask
  return (unshifted_num << 2) & mask # Using Word Addresses



def Address_Adder(next_pc, shifted_num):
  return next_pc + shifted_num



## Memory Access ##
#class Data_Memory(Memory):
#  def __init__(self, size):
#    Memory.__init__(self, size)
#
#  def Operate(self, address, write_data, MemRead, MemWrite):
#    read_data = 0
#
#    if MemRead:
#      read_data = Memory.Load_Word(self, address)
#    if MemWrite:
#      Memory.Store_Word(self, address, write_data)
#
#    return read_data



## Write Back ##
def Write_Back_Mux(Read_Data, ALU_Result, MemToReg):
  return MUX(ALU_Result, Read_Data, MemToReg)
