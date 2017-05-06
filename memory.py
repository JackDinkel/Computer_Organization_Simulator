import hardware as HW
import mask

class Memory(object):
  # NOTE: We decided to model this as a combination of word addressable and byte addressable
  # This is a divergence from lec 21, but I leave it here for reference
  # Outside this class, everything is byte addressable, as normal
  # Inside this class, memory is word addressed, so each list element stores a single word
  # Simply divide the address by 4 to get the index, and % by 4 to get the offset

  __data = []

  def __init__(self, size, contents = []):
      self.__data = contents
      for _ in xrange(size - len(self.__data)):
        self.__data.append(0)


  def Update(self, size, contents = []):
    self.__init__(size, contents)


  def __del__(self):
    self.__data = []


  def Direct_Update(self, address, data):
    # For testing...
    self.__data[address / 4] = data


  def Direct_Fetch(self, address):
    # For testing...
    return self.__data[address / 4]


  def display(self):
    print self.__data


  def Load(self, address, data_type = 'w'):
    index  = address / 4
    address_offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert address_offset >= 0 and address_offset < 4, "address offset out of bounds: %s" % address_offset
    assert data_type == 'w' or data_type == 'h' or data_type == 'hu' or data_type == 'b' or data_type == 'bu'

    word = self.__data[index]

    # Fetch word
    if   data_type == 'w':
      return HW.Sign_Extend(word, 32)

    # Fetch signed half
    elif data_type == 'h':
      assert address_offset == 0 or address_offset == 2, "offset out of bounds: %s" % address_offset
      return HW.Sign_Extend(mask.Get_Half(word, address_offset), 16)

    # Fetch unsigned half
    elif data_type == 'hu':
      assert address_offset == 0 or address_offset == 2, "offset out of bounds: %s" % address_offset
      return mask.Get_Half(word, address_offset)

    # Fetch signed byte
    elif data_type == 'b':
      assert address_offset >= 0 and address_offset < 4, "offset out of bounds: %s" % address_offset
      return HW.Sign_Extend(mask.Get_Byte(word, address_offset), 8)

    # Fetch unsigned byte
    elif data_type == 'bu':
      assert address_offset >= 0 and address_offset < 4, "offset out of bounds: %s" % address_offset
      return mask.Get_Byte(word, address_offset)

    else:
      assert 0 == 1, "invalid data_type: %s" % data_type


  def Store(self, address, data, data_type = 'w'):
    index = address / 4
    address_offset = address % 4
    assert len(self.__data) > 0, "Memory is empty!"
    assert index >= 0 and index < len(self.__data), "index out of bounds: %s in memory size %s" % (index, len(self.__data))
    assert HW.unsigned(data, 32) >= 0x0 and HW.unsigned(data, 32) <= 0xFFFFFFFF, "data out of bounds: %s" % data
    assert address_offset >= 0 and address_offset < 4
    assert data_type == 'w' or data_type == 'h' or data_type == 'b'

    # Store word
    if   data_type == 'w':
      self.__data[index] = data

    # Store half
    elif data_type == 'h':
      assert address_offset == 0 or address_offset == 2, "offset out of bounds: %s" % address_offset

      word = self.__data[index]
      self.__data[index] = mask.Insert_Half(word, data, address_offset)

    # Store byte
    elif data_type == 'b':
      assert address_offset >= 0 and address_offset < 4, "offset out of bounds: %s" % address_offset

      word = self.__data[index]
      self.__data[index] = mask.Insert_Byte(word, data, address_offset)

    else:
      assert 0 == 1, "invalid data_type: %s" % data_type


  def Data_Operate(self, address, write_data, MemRead, MemWrite, Op):
    read_data = 0

    if MemRead:
      assert Op >= 12 and Op <= 16, "Op out of bounds: %s" % Op
      if Op == ALU_DICT["LW"]:
        read_data = Memory.Load(address, 'w')
      if Op == ALU_DICT["LBU"]:
        read_data = Memory.Load(address, 'bu')
      if Op == ALU_DICT["LHU"]:
        read_data = Memory.Load(address, 'hu')

    if MemWrite:
      assert Op >= 17 and Op <= 19, "Op out of bounds: %s" % Op
      if Op == ALU_DICT["SB"]:
        Memory.Store(address, write_data, 'b')
      if Op == ALU_DICT["SH"]:
        Memory.Store(address, write_data, 'h')
      if Op == ALU_DICT["SW"]:
        Memory.Store(address, write_data, 'w')
      if Op == ALU_DICT["SLT"]:
        Memory.Store(address, write_data, 'w')

    return read_data


  def Instruction_Operate(self, address, write_data, MemRead, MemWrite):
    read_data = 0

    if MemRead:
      read_data = Memory.Load(address)
    if MemWrite:
      Memory.Store(address, write_data)

    return read_data