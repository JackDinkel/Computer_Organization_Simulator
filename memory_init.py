import cache
from control import ALU_DICT
from opcode import OP_DICT
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
      self.main_memory = m.Memory(mem_size, mem_contents)

      self.data_cache  = cache.Direct_Cache(data_cache_blocks,
                                              data_cache_words,
                                              cache_write_policy,
                                              self.main_memory
                                              )

      self.instr_cache = cache.Direct_Cache(instr_cache_blocks,
                                              instr_cache_words,
                                              cache_write_policy,
                                              self.main_memory
                                              )

    # Set up only memory
    elif cache_type == 'none':
      self.main_memory = m.Memory(mem_size, mem_contents)
      self.data_cache = m.Memory(mem_size, mem_contents)
      self.instr_cache = self.data_cache

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
    return self.main_memory.Direct_Fetch(address)

  def Direct_Store(self, address, data):
    self.main_memory.Direct_Update(address, data)

  def Data_Operate(self, address, write_data, MemRead, MemWrite, Op):
    read_data = 0

    if MemRead:
      if Op == OP_DICT["LW"]:
        read_data = self.data_cache.Load(address, 'w')
      elif Op == OP_DICT["LBU"]:
        read_data = self.data_cache.Load(address, 'bu')
      elif Op == OP_DICT["LHU"]:
        read_data = self.data_cache.Load(address, 'hu')

    if MemWrite:
      if Op == OP_DICT["SB"]:
        self.data_cache.Store(address, write_data, 'b')
      elif Op == OP_DICT["SH"]:
        self.data_cache.Store(address, write_data, 'h')
      elif Op == OP_DICT["SW"]:
        self.data_cache.Store(address, write_data, 'w')
      elif Op == OP_DICT["SLT"]:
        self.data_cache.Store(address, write_data, 'w')

    return read_data


  def Instruction_Operate(self, address, write_data, MemRead, MemWrite):
    read_data = 0

    if MemRead:
      read_data = self.instr_cache.Load(address)
    if MemWrite:
      self.instr_cache.Store(address, write_data)

    return read_data