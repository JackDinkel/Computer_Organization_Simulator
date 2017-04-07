import hardware as HW
import decode
import pytest
import single_cycle
from register import RegEnum


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



@pytest.mark.skip()
def test_Register_File():
  #TODO
  pass



@pytest.mark.skip()
def test_Sign_Extend():
  #TODO
  pass



@pytest.mark.skip()
def test_ALU():
  #TODO
  pass



def test_Shift_Left_2():
  v = 154
  assert HW.Shift_Left_2(v) == v << 2



@pytest.mark.skip()
def test_Data_Memory():
  #TODO
  pass



def test_addi():
  simulator = single_cycle.Single_Cycle()
  simulator.Instruction_Memory.Add_Word(0x20C60005) # addi a2 a2 0x5
  simulator.execute()


  a2_val = simulator.Register_File.Get(RegEnum.a2)
  assert a2_val == 0x05



def test_sll():
  simulator = single_cycle.Single_Cycle()
  simulator.Instruction_Memory.Add_Word(0x00063080) # sll a2,a2,0x2
  simulator.execute()
