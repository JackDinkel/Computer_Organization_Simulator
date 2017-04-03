from hardware import *
import pytest


def test_mux():
  assert MUX("hi", 123, 0) == "hi"
  assert MUX("hi", 123, 1) == 123

def test_PC():
  v = 0
  mypc = PC(v)
  assert mypc.Get() == v

  v = 400
  mypc.Update(v)
  assert mypc.Get() == v

@pytest.mark.skip()
def test_Instruction_Memory():
  #TODO
  pass

def test_Add_Four():
  v = 12
  assert Add_Four(v) == v + 4

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
  assert Shift_Left_2(v) == v << 2

@pytest.mark.skip()
def test_Data_Memory():
  #TODO
  pass
