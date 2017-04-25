import hardware as HW
import decode
import pytest
import single_cycle
from control import ALU_DICT
from register import REG_DICT


def test_mux():
  assert HW.MUX("hi", 123, 0) == "hi"
  assert HW.MUX("hi", 123, 1) == 123



def test_PC():
  v = 0
  mypc = HW.PC()
  assert mypc.Get() == v

  v = 400
  mypc.Update(v)
  assert mypc.Get() == v



def test_Decode():
  decoder = decode.Decoder()

  instr = 0x00000000
  decoder.decode(instr)
  assert decoder.op == 0x0
  assert decoder.rs == 0x0
  assert decoder.rt == 0x0
  assert decoder.rd == 0x0
  assert decoder.shamt == 0x0
  assert decoder.funct == 0x0
  assert decoder.i_imm == 0x0
  assert decoder.j_imm == 0x0

  # subu t4,t5,t3
  instr = 0x01ab6023 
  decoder.decode(instr)
  assert decoder.op == 0x0
  assert decoder.rs == 0xD
  assert decoder.rt == 0xB
  assert decoder.rd == 0xC
  assert decoder.shamt == 0x0
  assert decoder.funct == 0x23

  # addiu t5,a1,-1
  instr = 0x24adffff 
  decoder.decode(instr)
  assert decoder.op == 0x9
  assert decoder.rs == 0x5
  assert decoder.rt == 0xD
  assert decoder.i_imm == 0xFFFF

  # jal 120
  instr = 0x0c000078 
  decoder.decode(instr)
  assert decoder.op == 0x3
  assert decoder.j_imm == 0x78



def test_Register_File():
  f = HW.Register_File()

  a1 = REG_DICT["a1"]
  t1 = REG_DICT["t1"]
  value = 0x100
  RegWriteOn = 1
  RegWriteOff = 0

  # Check if a1 and t1 are zero
  assert f.Operate(a1, t1, t1, value, RegWriteOff) == (0, 0)
  assert f.Get(a1) == 0
  assert f.Get(t1) == 0

  # Load 0x100 into t1
  # Check that a1 is 0 and t1 is 0x100
  assert f.Operate(a1, t1, t1, value, RegWriteOn) == (0, value)
  assert f.Get(a1) == 0
  assert f.Get(t1) == value

  # Check that a1 is 0 and t1 is 0x100
  assert f.Operate(a1, t1, t1, value, RegWriteOff) == (0, value)
  assert f.Get(a1) == 0
  assert f.Get(t1) == value




def test_Sign_Extend():
  val1 = 0b1111111111110000 # -16
  val2 = 0xFFFF # -1
  val3 = 0xFFCE # -50
  val4 = 0x0064 # 100
  val5 = 0x0000 # 0

  assert HW.Sign_Extend(val1) == 0b11111111111111111111111111110000
  assert HW.Sign_Extend(val2) == 0b11111111111111111111111111111111
  assert HW.Sign_Extend(val3) == 0b11111111111111111111111111001110
  assert HW.Sign_Extend(val4) == 0b00000000000000000000000001100100
  assert HW.Sign_Extend(val5) == 0b00000000000000000000000000000000




def test_ALU():
  #TODO
  input1 = 5
  input2 = 2
  shamt = 3

  #assert HW.ALU(input1, input2, 0, ALU_DICT["X"])     == (0, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["AND"])   == (input1 & input2, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["OR"])    == (input1 | input2, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["ADD"])   == (input1 + input2, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["ADDU"])  == (input1 + input2, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["SUB"])   == (input1 - input2, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SUBU"])  == (input1 - input2, 0) # TODO
  assert HW.ALU(input1, input2,shamt,ALU_DICT["SLL"]) == (input2 << shamt, 0)
  assert HW.ALU(input1, input2,shamt,ALU_DICT["SRL"]) == (input2 >> shamt, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SLT"])   == (0, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["SLTU"])  == (0, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["NOT"])   == (~input1, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["LOAD"])  == (7, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["STORE"]) == (7, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["NOR"])   == (~(input1 | input2), 0) # TODO



def test_add_shift():
  instruction1 = 0x20C60005 # addi a2 a2 0x5
  instruction2 = 0x00063080 # sll a2,a2,0x2
  a2 = REG_DICT["a2"]

  simulator = single_cycle.Single_Cycle()
  simulator.Instruction_Memory.Store_Word(0, instruction1)
  simulator.Instruction_Memory.Store_Word(1, instruction2)
  simulator.cycle()

  # Check register
  a2_val = simulator.Register_File.Get(a2)
  assert a2_val == 0x05

  simulator.cycle()
  a2_val = simulator.Register_File.Get(a2)
  assert a2_val == 0b10100



def test_signed_add():
  instruction = 0x27bdfff0 # addiu sp,sp,-16
  simulator = single_cycle.Single_Cycle()
  simulator.Instruction_Memory.__init__(5)
  simulator.Data_Memory.__init__(5)
  simulator.Register_File.__init__()
  simulator.Instruction_Memory.Store_Word(0, instruction)
  simulator.cycle()

  sp = REG_DICT["sp"]
  sp_val = simulator.Register_File.Get(sp)
  print simulator.decoder.i_imm
  print sp_val
  assert sp_val == -16

def test_memory():
  instruction1 = 0x214A0005 # addi t2 t2 0x5
  instruction2 = 0xAFAA0000 # sw t2, 0(sp)
  instruction3 = 0x8FA70000 # lw a3, 0(sp)
  
  t2 = REG_DICT["t2"]
  a3 = REG_DICT["a3"]

  simulator = single_cycle.Single_Cycle()
  simulator.Instruction_Memory.__init__(5)
  simulator.Data_Memory.__init__(5)
  simulator.Register_File.__init__()
  simulator.Instruction_Memory.Store_Word(0, instruction1)
  simulator.Instruction_Memory.Store_Word(1, instruction2)
  simulator.Instruction_Memory.Store_Word(2, instruction3)
  simulator.cycle()

  # Check register
  t2_val = simulator.Register_File.Get(t2)
  assert t2_val == 0x05

  #simulator.Data_Memory.display()
  #print simulator.Register_File.GetList()
  simulator.cycle()
  #simulator.Data_Memory.display()
  assert simulator.Data_Memory.Load_Word(0) == t2_val

  assert simulator.Register_File.Get(a3) == 0
  simulator.cycle()
  print simulator.decoder.display()
  print simulator.controller.display()
  assert simulator.Register_File.Get(a3) == t2_val

