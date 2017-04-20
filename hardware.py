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
    assert new_val >= 0x0 and new_val <= 0xFFFFFFFF, "new_val out of bounds: %s" % new_val
    self.__value = new_val

  def Get(self):
    return self.__value


class Memory(object):
  # A list of all instructions
  __data = []

  def Fetch_Word(self, address):
    assert len(self.__data) > 0, "Memory is empty!"
    assert address >= 0 and address < len(self.__data), "address out of bounds: %s" % address
    return self.__data[address]
    
  def Add_Word(self, data):
    assert data >= 0x0 and data <= 0xFFFFFFFF, "data out of bounds: %s" % data

    # A word is 4 bytes, simulate this by having 3 empty slots
    # NOTE: would it be better to split this up by word? Other ideas? See above.
    #       What if we make the memories a fixed size of registers.
    #       Then, each register can have byte operations (that just use masking).
    #       Divide by four when doing a memory operation and it all should work...
    self.__data.append(data)
    self.__data.append(0)
    self.__data.append(0)
    self.__data.append(0)

  def Load_Word(self, address, data):
    assert len(self.__data) > 0, "Memory is empty!"
    assert address >= 0 and address < len(self.__data), "address out of bounds: %s" % address
    assert data >= 0x0 and data <= 0xFFFFFFFF, "data out of bounds: %s" % data
    self.__data[address] = data



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
  pass



def Add_Four(input_num):
  #TODO: Error bounds
  return input_num + 4



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
    assert write_data >= 0x0 and write_data <= 0xFFFFFFFF, "write_data out of bounds: %s" % write_data
    assert RegWrite == 0 or RegWrite == 1, "RegWrite out of bounds: %s" % RegWrite

    if RegWrite:
      self.__register_list[write_reg].Update(write_data)

    read_data_1 = self.__register_list[read_reg_1].Get()
    read_data_2 = self.__register_list[read_reg_2].Get()

    return read_data_1, read_data_2



def Sign_Extend(input_val):
  # Sign extend a 16 bit number to 32 bits

  def twos_comp(val, num_bits):
  # Returns num_bits bit 2's comp interpreted value
    if (val & (1 << (num_bits - 1))) != 0:
      val = val - (1 << num_bits)
    return val

  twos_val = twos_comp(input_val, 16)
  return twos_val if twos_val >= 0 else (twos_val + 0x100000000)


## Execute and Address Calculation ##
def ALU_Input_Mux(register, sign_extended, ALUSrc):
  return MUX(register, sign_extended, ALUSrc)



def ALU(input1, input2, shamt, ALUControl):
  # TODO: How does this interface with ALU Control? What is the zero Zero line on page 265?
  if   ALUControl == ALU_DICT["X"]:
    return 0, 0
  elif ALUControl == ALU_DICT["AND"]:
    return input1 & input2, 0
  elif ALUControl == ALU_DICT["OR"]:
    return input1 | input2, 0
  elif ALUControl == ALU_DICT["ADD"]:
    return input1 + input2, 0
  elif ALUControl == ALU_DICT["ADDU"]:
    return input1 + input2, 0 # TODO
  elif ALUControl == ALU_DICT["SUB"]:
    return input1 - input2, 0
  elif ALUControl == ALU_DICT["SUBU"]:
    return input1 - input2, 0 # TODO
  elif ALUControl == ALU_DICT["SLL"]:
    return input2 << shamt, 0
  elif ALUControl == ALU_DICT["SRL"]:
    return input2 >> shamt if input2 >= 0 else (input2 + 0x100000000) >> shamt, 0
  elif ALUControl == ALU_DICT["SLT"]:
    return (input1 < input2), 0 # TODO
  elif ALUControl == ALU_DICT["SLTU"]:
    return (input1 < input2), 0 # TODO
  elif ALUControl == ALU_DICT["NOT"]:
    return ~input1, 0 # TODO
  elif ALUControl == ALU_DICT["LOAD"]:
    return 0, 0, # TODO
  elif ALUControl == ALU_DICT["STORE"]:
    return 0, 0 # TODO
  elif ALUControl == ALU_DICT["NOR"]:
    return ~(input1 | input2), 0 # TODO
  else:
    assert 1 == 2, "Invalid Operation: %s" % ALUControl



def Shift_Left_2(unshifted_num):
  return unshifted_num << 2



def Calculate_Jump_Addr(unshifted_num, next_pc):
  # This takes the place of the shift left 2 and concatenation components on page 271
  # TODO: assert unshifted_num is in bounds (26 bits)
  mask = 0xF0000000
  pc_upper = next_pc & mask
  return (unshifted_num << 2) & mask



def Address_Adder(next_pc, shifted_num):
  return next_pc + shifted_num



## Memory Access ##
class Data_Memory(Memory):
  def Operate(self, address, write_data, MemRead, MemWrite):
    read_data = 0

    if MemRead:
      read_data = Memory.Fetch_Word(address)
    if MemWrite:
      Memory.Load_Word(address, write_data)

    return read_data



## Write Back ##
def Write_Back_Mux(Read_Data, ALU_Result, MemToReg):
  return MUX(ALU_Result, Read_Data, MemToReg)
