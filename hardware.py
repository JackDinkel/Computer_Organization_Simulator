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



# General Functions
def MUX(input1, input2, control):
  assert control == 0 or control == 1, "control out of bounds: %s" % control

  if control == 0:
    return input1
  else:
    return input2



##### Hardware ######

## Instruction Fetch ##
def PC_Input_Mux(incremented, jump, PCSrc):
  return MUX(incremented, jump, PCSrc)

class PC:
  __pc = 0

  def __init__(self, init_val):
    self.__pc = init_val

  def Update(self, new_val):
    assert new_val >= 0x0 and new_val <= 0xFFFFFFFF, "new_val out of bounds: %s" % new_val
    self.__pc = new_val

  def Get(self):
    return self.__pc

class Instruction_Memory:
  # A list of all instructions
  __Memory = []

  def Fetch_Instruction(self, address):
    assert len(self.__Memory) > 0, "Instruction Memory is empty!"
    assert address >= 0 and address < len(self.__Memory), "address out of bounds: %s" % address
    return self.__Memory[address]

  def Add_New_Instruction(self, instr):
    assert instr >= 0x0 and instr <= 0xFFFFFFFF, "instr out of bounds: %s" % instr

    # Instructions are 4 bytes, simulate this by having 3 empty slots
    self.__Memory.append(instr)
    self.__Memory.append(0)
    self.__Memory.append(0)
    self.__Memory.append(0)

def Add_Four(input_num):
  #TODO: Error bounds
  return input_num + 4

def Register_Input_Mux(i_type_reg, r_type_reg, RegDst):
  return MUX(i_type_reg, r_type_reg, RegDst)
  

## Instruction Decode and Register File Read ##
class Register_File:
  class Register:
    __value = 0

    def __init__(self):
      self.__value = 0

  register_list = []

  def __init__(self):
    for _ in len(range(32)):
      # Initialize list of 32 registers
      self.register_list = [ Register() for _ in range(32) ]
  
  def Operate(self, read_reg_1, read_reg_2, write_reg, write_data, RegWrite):
    assert read_reg_1 >= 0 and read_reg_1 < 32, "read_reg_1 out of bounds: %d" % read_reg_1
    assert read_reg_2 >= 0 and read_reg_2 < 32, "read_reg_2 out of bounds: %d" % read_reg_2
    assert write_reg  >= 0 and write_reg  < 32, "write_reg out of bounds: %d" % write_reg
    #TODO: assert write_data in range

    #return read_data_1, read_data_2

def Sign_Extend(input_num):
  # Return a 32 bit sign extended number
  pass


## Execute and Address Calculation ##
def ALU_Input_Mux(register, sign_extended, ALUSrc):
  return MUX(register, sign_extended, ALUSrc)

def ALU(input1, input2, ALUOperation):
  pass

def Shift_Left_2(unshifted_num):
  return unshifted_num << 2

def Address_Adder(next_pc, shifted_num):
  return next_pc + shifted_num


## Memory Access ##
class Data_Memory:
  def Operate(self, address, write_data, MemWrite, MemRead):
    # return read_data
    pass

## Write Back ##
def Write_Back_Mux(Read_Data, ALU_Result, MemToReg):
  return MUX(Read_Data, ALU_Result, MemToReg)
