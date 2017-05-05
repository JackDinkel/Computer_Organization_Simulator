from globals import *

REG_DICT = {
  "zero" : 0,
  "at" : 1,
  "v0" : 2,
  "v1" : 3,
  "a0" : 4,
  "a1" : 5,
  "a2" : 6,
  "a3" : 7,
  "t0" : 8,
  "t1" : 9,
  "t2" : 10,
  "t3" : 11,
  "t4" : 12,
  "t5" : 13,
  "t6" : 14,
  "t7" : 15,
  "s0" : 16,
  "s1" : 17,
  "s2" : 18,
  "s3" : 19,
  "s4" : 20,
  "s5" : 21,
  "s6" : 22,
  "s7" : 23,
  "t8" : 24,
  "t9" : 25,
  "k0" : 26,
  "k1" : 27,
  "gp" : 28,
  "sp" : 29,
  "fp" : 30,
  "ra" : 31
}


class Register(object):
  __value = 0

  def __init__(self):
    self.__value = 0

  def Set(self, new_val):
    assert unsigned(new_val, 32) >= 0x0 and unsigned(new_val, 32) <= 0xFFFFFFFF, "new_val out of bounds: %s" % new_val
    self.__value = new_val

  def Get(self):
    return self.__value



class PC(Register):
  pass


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

    if RegWrite and write_reg != 0:
      self.__register_list[write_reg].Set(write_data)

    read_data_1 = self.__register_list[read_reg_1].Get()
    read_data_2 = self.__register_list[read_reg_2].Get()

    return read_data_1, read_data_2
