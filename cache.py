
# on hit, proceed normally

# on miss,
#  stall the pipeline
#  fetch memory into cache
#  restart IF or finish data access

# Instr cache miss
'''
halt the processor
send PC - 4 to main memory
put data from memory in cache, set tag and valid bit
restart IF - it will have a cache hit!
'''

# Write thru
'''
On a hit:
  Write data to cache, then to a buffer
  restart CPU
  How do we update the buffer???
On a miss:
  Write allocate, fetch the block into cache
  Do we write to memory first or after???
'''

# Write Back
'''
On a hit:
  Write data to cache, keep track of dirty blocks
  When a dirty block is evicted, write to a buffer
  Put new block into cache
  restart CPU
  How do we update from the buffer???
    Write the data in the write buffer to main memory
    Writing to main memory blocks support for all memory access for
     6 cycles on the first word and 2 cycles for each additional block
On a miss:
  fetch the block into the cache
  Do we write to memory first or after???
'''

# Direct Mapped
'''
List of blocks
Each block is a list of three things, valid, tag, data
  data is a list of words
'''

import mask
from globals import *
import hardware as HW
from math import log, ceil

class Direct_Cache(object):

  def __init__(self, blocks, words, writePolicy, memory):
    assert writePolicy == "through" or writePolicy == "back", "invalid write policy: %s" % writePolicy

    # Set attributes
    self.num_blocks = blocks
    self.num_words = words
    self.write_policy = writePolicy

    # Build the empty cache
    self.__data = [ [0, 0, [0 for _ in range(self.num_words)] ] for _ in xrange(self.num_blocks) ]

    # Initialize memory
    self.memory = memory


  def Update(self, blocks, words, writePolicy, memory):
    # Call to change the rebuild a new empty cache
    self.__init__(blocks, words, writePolicy, memory)


  def Direct_Update(self, index, update):
    # For testing only
    self.__data[index] = update


  def Direct_Fetch(self, index):
    # For testing only
    return self.__data[index]


  def display(self):
    print self.__data


  def Address_Decode(self, address):
    assert address >= 0 and address <= 0xFFFFFFFF, "Address out of bounds: %s" % address

    # Interpret an address
    num_byte_offset_bits = 2
    num_word_offset_bits = int(ceil(log(self.num_words, 2)))
    num_index_bits = int(ceil(log(self.num_blocks, 2)))
    num_tag_bits = 32 - num_index_bits - num_word_offset_bits - num_byte_offset_bits

    # Calculate masks
    word_offset_mask = mask.Generate_Right_Mask(num_word_offset_bits) << num_byte_offset_bits
    index_mask = mask.Generate_Right_Mask(num_index_bits) << (num_byte_offset_bits + num_word_offset_bits)
    tag_mask = mask.Generate_Right_Mask(num_tag_bits) << (32 - num_tag_bits)

    # Calculate fields
    word_offset = logical_rshift(address & word_offset_mask, num_byte_offset_bits)
    index = logical_rshift(address & index_mask, num_byte_offset_bits + num_word_offset_bits)
    tag = logical_rshift(address & tag_mask, num_byte_offset_bits + num_word_offset_bits + num_index_bits)

    return tag, index, word_offset


  def Address_Encode(self, tag, index, word_offset, byte_offset):
    # Interpret an address
    num_byte_offset_bits = 2
    num_word_offset_bits = int(ceil(log(self.num_words, 2)))
    num_index_bits = int(ceil(log(self.num_blocks, 2)))
    num_tag_bits = 32 - num_index_bits - num_word_offset_bits - num_byte_offset_bits

    address = (tag << 32 - num_tag_bits) | (index << (num_word_offset_bits + num_byte_offset_bits)) | \
              (word_offset << num_byte_offset_bits) | byte_offset

    assert address >= 0 and address <= 0xFFFFFFFF, "Calculated address out of bounds: %s" % address
    return address


  def Validate(self, index):
    # Return 1 if address is a hit, 0 if miss
    return self.__data[index][0]


  def Matching_Tags(self, index, tag):
    # Return 1 if tags match, 0 if not
    return self.__data[index][1] == tag


  def Load_Block_From_Memory(self, address):
    # Load the entire block to cache from memory
    tag, index, word_offset = self.Address_Decode(address)
    block_address = self.Address_Encode(tag, index, 0, 0)
    block = []
    for word in xrange(self.num_words):
      addr = block_address + (word * 4)
      wd = self.memory.Load(addr)
      block.append(wd)
    assert len(block) == self.num_words
    self.__data[index][2] = block
    self.__data[index][1] = tag
    self.__data[index][0] = 1

    # For testing...
    return block


  def Store_Block_To_Memory(self, address):
    # Store the entire block to memory from cache
    tag, index, word_offset = self.Address_Decode(address)
    block_address = self.Address_Encode(tag, index, 0, 0)
    block = self.__data[index][2]
    assert len(block) == self.num_words
    for word in xrange(self.num_words):
      addr = block_address + (word * 4)
      wd = block[word]
      self.memory.Store(addr, wd)

    # For testing...
    return block
    
    
  def Store(self, address, data, data_type = 'w'):
    def write_back(index, word_offset):
      # Write block to memory
      evictee_tag = self.__data[index][1]
      evictee_address = self.Address_Encode(evictee_tag, index, word_offset, 0)
      evictee_data = self.__data[index][2]
      self.Store_Block_To_Memory(evictee_address)

    def evict_and_load(address):
      # Evict old block and load new block from memory
      tag, index, word_offset = self.Address_Decode(address)
      # Write old block to memory if necessary
      if self.write_policy == "back":
        write_back(index, word_offset)
      self.Load_Block_From_Memory(address)

    address_offset = address % 4
    assert address >= 0 and address <= 0xFFFFFFFF, "Address out of bounds: %s" % address
    assert data_type == 'w' or data_type == 'h' or data_type == 'b'
    assert address_offset >= 0 and address_offset < 4, "offset out of bounds: %s" % address_offset

    tag, index, word_offset = self.Address_Decode(address)

    # Cache miss
    if not self.Validate(index):
      self.Load_Block_From_Memory(address)
      return "miss" # TODO: Probably also need to return number of cycles penalized

    # Need to evict
    if not self.Matching_Tags(index, tag):
      evict_and_load(address)

    ## Cache hit, write
    # Write a word
    if   data_type == 'w':
      self.__data[index][2][word_offset] = data

    # Write a half
    elif data_type == 'h':
      assert address_offset == 0 or address_offset == 2, "offset out of bounds: %s" % address_offset

      word = self.__data[index][2][word_offset]
      self.__data[index][2][word_offset] = mask.Insert_Half(word, data, address_offset)

    # Write a byte
    elif data_type == 'b':
      assert address_offset >= 0 and address_offset < 4, "offset out of bounds: %s" % address_offset

      word = self.__data[index][2][word_offset]
      self.__data[index][2][word_offset] = mask.Insert_Byte(word, data, address_offset)

    else:
      assert 0 == 1, "invalid data_type: %s" % data_type

    # Write through
    if self.write_policy == "through":
      self.Store_Block_To_Memory(address)

    return 'hit'


  def Load(self, address, data_type = 'w'):
    address_offset = address % 4
    assert address_offset >= 0 and address_offset < 4, "offset out of bounds: %s" % address_offset
    assert address >= 0 and address <= 0xFFFFFFFF, "Address out of bounds: %s" % address
    assert data_type == 'w' or data_type == 'h' or data_type == 'hu' or data_type == 'b' or data_type == 'bu'

    tag, index, word_offset = self.Address_Decode(address)

    # Cache miss
    if not self.Validate(index):
      self.Load_Block_From_Memory(address)
      return "miss" # TODO: Probably also need to return number of cycles penalized

    ## Cache hit, fetch
    word = self.__data[index][2][word_offset] # Load word

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

