import cache
import memory as m

class memory(object):
  def __init__(self,
               cache_type,
               cache_write_policy,
               data_cache_blocks,
               data_cache_words,
               instr_cache_blocks,
               instr_cache_words,
               mem_size,
               mem_contents = []
               ):

    assert cache_type == 'direct' or cache_type == 'none'
    assert cache_write_policy == "through" or cache_write_policy == "back", "invalid write policy: %s" % cache_write_policy

    # Set up direct cache
    if cache_type == 'direct':
      self.__main_memory = m.Memory(mem_size, mem_contents)

      self.__data_cache  = cache.Direct_Cache(data_cache_blocks,
                                              data_cache_words,
                                              cache_write_policy,
                                              self.__main_memory
                                              )

      self.__instr_cache = cache.Direct_Cache(instr_cache_blocks,
                                              instr_cache_words,
                                              cache_write_policy,
                                              self.__main_memory
                                              )

    # Set up only memory
    elif cache_type == 'none':
      __data_cache = m.Memory(mem_size, mem_contents)
      __instr_cache = __data_cache

    else:
      assert 0 == 1, "invalid cache type: %s" % cache_type


  
  def Update(self,
             cache_type,
             cache_write_policy,
             data_cache_blocks,
             data_cache_words,
             instr_cache_blocks,
             instr_cache_words,
             mem_size,
             mem_contents = []
             ):

    self.__init__(cache_type,
                  cache_write_policy,
                  data_cache_blocks,
                  data_cache_words,
                  instr_cache_blocks,
                  instr_cache_words,
                  mem_size,
                  mem_contents = []
                  )


  def Direct_Load(self, address):
    return self.__data_cache.Direct_Load(address)


  def Data_Operate(self, address, write_data, MemRead, MemWrite, Op):
    read_data = 0

    if MemRead:
      assert Op >= 12 and Op <= 16, "Op out of bounds: %s" % Op
      if Op == ALU_DICT["LW"]:
        read_data = self.__data_cache.Load(address, 'w')
      if Op == ALU_DICT["LBU"]:
        read_data = self.__data_cache.Load(address, 'bu')
      if Op == ALU_DICT["LHU"]:
        read_data = self.__data_cache.Load(address, 'hu')

    if MemWrite:
      assert Op >= 17 and Op <= 19, "Op out of bounds: %s" % Op
      if Op == ALU_DICT["SB"]:
        self.__data_cache.Store(address, write_data, 'b')
      if Op == ALU_DICT["SH"]:
        self.__data_cache.Store(address, write_data, 'h')
      if Op == ALU_DICT["SW"]:
        self.__data_cache.Store(address, write_data, 'w')
      if Op == ALU_DICT["SLT"]:
        self.__data_cache.Store(address, write_data, 'w')

    return read_data


  def Instruction_Operate(self, address, write_data, MemRead, MemWrite):
    read_data = 0

    if MemRead:
      read_data = self.__instr_cache.Load(address)
    if MemWrite:
      self.__instr_cache.Store(address, write_data)

    return read_data


