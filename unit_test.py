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


@pytest.mark.skip()
def test_Instruction_Memory():
  #TODO
  pass



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


def test_Add_Four():
  v = 12
  assert HW.Add_Four(v) == v + 4



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




@pytest.mark.skip()
def test_Sign_Extend():
  #TODO
  pass



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
  assert HW.ALU(input1, input2, 0, ALU_DICT["LOAD"])  == (0, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["STORE"]) == (0, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["NOR"])   == (~(input1 | input2), 0) # TODO





def test_Shift_Left_2():
  v = 154
  assert HW.Shift_Left_2(v) == v << 2



@pytest.mark.skip()
def test_Data_Memory():
  #TODO
  pass



def test_add_shift():
  instruction1 = 0x20C60005 # addi a2 a2 0x5
  instruction2 = 0x00063080 # sll a2,a2,0x2
  a2 = REG_DICT["a2"]

  simulator = single_cycle.Single_Cycle()
  simulator.Instruction_Memory.Add_Word(instruction1)
  simulator.Instruction_Memory.Add_Word(instruction2)
  simulator.cycle()

  # Check register
  a2_val = simulator.Register_File.Get(a2)
  assert a2_val == 0x05

  simulator.cycle()
  a2_val = simulator.Register_File.Get(a2)
  assert a2_val == 0b10100


