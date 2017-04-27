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
from opcode import OP_DICT
from globals import *

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

  def Update(self, new_val):
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

  def __init__(self, size):
    self.__data = [0 for _ in xrange(size)]

  def __del__(self):
    self.__data = []

  def Load_Word(self, address):
    index = address / 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    return self.__data[index]

  def Load_Half(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    word = twos_comp(self.__data[index])
    return Sign_Extend(mask.Get_Half(word, offset))

  def Load_Half_Unsigned(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    word = twos_comp(self.__data[index])
    return mask.Get_Half(word, offset)

  def Load_Byte(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    word = twos_comp(self.__data[index])
    return Sign_Extend(mask.Get_Byte(word, offset))

  def Load_Byte_Unsigned(self, address):
    index  = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    word = twos_comp(self.__data[index])
    return mask.Get_Byte(word, offset)
    
  def Store_Word(self, address, data):
    index = address / 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    assert unsigned(data, 32) >= 0x0 and unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    self.__data[index] = data

  def Store_Half(self, address, data):
    index = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    assert unsigned(data, 32) >= 0x0 and unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    assert offset >= 0 and offset < 2

    shamt = offset * 16

    # Get current word
    word = self.Load_Word(address, data)
    mask = 0xFFFF << shamt
    shifted_word = word & mask

    # Update current word
    shifted_data = data << shamt
    word_to_write = shifted_word | sifted_data

    # Write updated word
    self.__data[index] = word_to_write

  def Store_Byte(self, address, data):
    index = address / 4
    offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "address out of bounds: %s" % address
    assert unsigned(data, 32) >= 0x0 and unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    assert offset >= 0 and offset < 4

    shamt = offset * 8

    # Get current word
    word = self.Load_Word(address, data)
    mask = 0xFF << shamt
    shifted_word = word & mask

    # Update current word
    shifted_data = data << shamt
    word_to_write = shifted_word | sifted_data

    # Write updated word
    self.__data[index] = word_to_write

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



class Instruction_Memory(Memory):
  def __init__(self, size):
    Memory.__init__(self, size)



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

  def Operate(self, read_reg_1, read_reg_2, write_reg, write_data, RegWrite):
    assert read_reg_1 >= 0 and read_reg_1 < 32, "read_reg_1 out of bounds: %d" % read_reg_1
    assert read_reg_2 >= 0 and read_reg_2 < 32, "read_reg_2 out of bounds: %d" % read_reg_2
    assert write_reg  >= 0 and write_reg  < 32, "write_reg out of bounds: %d" % write_reg
    assert unsigned(write_data, 32) >= 0x0 and unsigned(write_data, 32) <= 0xFFFFFFFF, "write_data out of bounds: %s" % write_data
    assert RegWrite == 0 or RegWrite == 1, "RegWrite out of bounds: %s" % RegWrite

    if RegWrite and write_reg != 0:
      self.__register_list[write_reg].Update(write_data)

    read_data_1 = self.__register_list[read_reg_1].Get()
    read_data_2 = self.__register_list[read_reg_2].Get()

    return read_data_1, read_data_2



def Sign_Extend(input_val, num_bits):
  # Sign extend to 32 bits
  twos_val = twos_comp(input_val, num_bits)
  return twos_val if twos_val >= 0 else (twos_val + 0x100000000)


def Hazard_Detection_Unit(memread, idex_rt, ifid_rs, ifid_rt):
  if ((memread == 1) and ((idex_rt == ifid_rt) or (idex_rt == ifid_rs))):
    return 1
  else:
    return 0


def Hazard_Detection_Mux(exc, memc, wbc, hazard):
  if hazard == 1:
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 0
    wbc.RegWrite  = 0
    exc.ALUOp     = 0
  return exc, memc, wbc



## Execute and Address Calculation ##
def ALU_Input_Mux(register, sign_extended, ALUSrc):
  return MUX(register, sign_extended, ALUSrc)



def ALU(input1, input2, shamt, ALUControl):
  if   ALUControl == ALU_DICT["X"]:
    return 0
  elif ALUControl == ALU_DICT["AND"]:
    return input1 & input2
  elif ALUControl == ALU_DICT["OR"]:
    return input1 | input2
  elif ALUControl == ALU_DICT["ADD"]:
    input1 = twos_comp(input1, 32)
    input2 = twos_comp(input2, 32)
    return input1 + input2
  elif ALUControl == ALU_DICT["ADDU"]:
    return input1 + input2 # TODO
  elif ALUControl == ALU_DICT["SUB"]:
    input1 = twos_comp(input1, 32)
    input2 = twos_comp(input2, 32)
    return input1 - input2
  elif ALUControl == ALU_DICT["SUBU"]:
    return input1 - input2 # TODO
  elif ALUControl == ALU_DICT["SLL"]:
    return input2 << shamt
  elif ALUControl == ALU_DICT["SRL"]:
    return logical_rshift(input2, shamt)
  elif ALUControl == ALU_DICT["SLT"]:
    return (input1 < input2) # TODO
  elif ALUControl == ALU_DICT["SLTU"]:
    return (input1 < input2) # TODO
  elif ALUControl == ALU_DICT["NOT"]:
    return ~input1 # TODO
  elif ALUControl == ALU_DICT["LOAD"]:
    return input1 + input2
  elif ALUControl == ALU_DICT["STORE"]:
    return input1 + input2
  elif ALUControl == ALU_DICT["NOR"]:
    return ~(input1 | input2) # TODO
  else:
    assert 1 == 2, "Invalid Operation: %s" % ALUControl



def Shift_Left_2(unshifted_num):
  return unshifted_num << 2 # Using Word Addresses



def Calculate_Jump_Addr(unshifted_num, next_pc):
  # This takes the place of the shift left 2 and concatenation components on page 271
  # TODO: assert unshifted_num is in bounds (26 bits)
  mask = 0xF0000000
  pc_upper = next_pc & mask
  return (unshifted_num << 2) + pc_upper # Using Word Addresses



def Address_Adder(next_pc, shifted_num):
  return next_pc + shifted_num



# see figures 4.56 and 4.57
def Forwarding_Unit(idex_rs, idex_rt, exmem_rd, memwb_rd, exmem_reg_write, memwb_reg_write):
  forwardA = 0
  forwardB = 0

  if (exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rs):
    forwardA = 2

  if (exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rt):
    forwardB = 2

  if ((memwb_reg_write == 1) and (memwb_rd != 0) and 
    not ((exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rs)) 
    and (memwb_rd == idex_rs)):
    forwardA = 1

  if ((memwb_reg_write == 1) and (memwb_rd != 0) and 
    not ((exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rt)) 
    and (memwb_rd == idex_rt)):
    forwardB = 1

  return forwardA, forwardB



def ALU_Reg_A_Mux(reg_data_1, write_back, alu_result, forwardA):
  assert forwardA >= 0 and forwardA <= 2, "forwardA out of bounds: %d" % forwardA
  if forwardA == 0:
    return reg_data_1
  elif forwardA == 1:
    return write_back
  elif forwardA == 2:
    return alu_result
  else:
    return 0



def ALU_Reg_B_MUX(reg_data_2, write_back, alu_result, forwardB):
  assert forwardB >= 0 and forwardB <= 2, "forwardB out of bounds: %d" % forwardB
  if forwardB == 0:
    return reg_data_2
  elif forwardB == 1:
    return write_back
  elif forwardB == 2:
    return alu_result
  else:
    return 0



## Memory Access ##
class Data_Memory(Memory):
  def __init__(self, size):
    Memory.__init__(self, size)

  def Operate(self, address, write_data, MemRead, MemWrite, op):
    read_data = 0

    if MemRead and OP_DICT["LW"]:
      read_data = Memory.Load_Word(self, address)
    elif MemRead and OP_DICT["LHU"]:
      read_data = Memory.Load_Half_Unsigned(self, address)
    elif MemRead and OP_DICT["LBU"]:
      read_data = Memory.Load_Byte_Unsigned(self, address)

    if MemWrite and OP_DICT["SW"]:
      Memory.Store_Word(self, address, write_data)
    elif MemWrite and OP_DICT["SH"]:
      Memory.Store_Half(self, address, write_data)
    elif MemWrite and OP_DICT["SB"]:
      Memory.Store_Byte(self, address, write_data)

    return read_data



## Write Back ##
def Write_Back_Mux(Read_Data, ALU_Result, MemToReg):
  return MUX(ALU_Result, Read_Data, MemToReg)
