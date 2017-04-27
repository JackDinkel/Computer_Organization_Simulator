
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
from math import log, ceil

class Direct_Cache(object):

  def __init__(self, blocks, words, writePolicy):
    assert writePolicy == "through" or writePolicy == "back", "invalid write policy: %s" % writePolicy

    # Set attributes
    self.num_blocks = blocks
    self.num_words = words
    self.write_policy = writePolicy

    # Build the empty cache
    self.__cache = [ 0, 0, []*self.num_words ] * self.num_blocks


  def Update(self, blocks, words):
    # Call to change the rebuild a new empty cache
    self.__init__(blocks, words)


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

    address = (tag << 32 - num_tag_bits) | (index << (num_word_offset_bits + num_byte_offset_bits)) | 
              (word_offset << num_byte_offset_bits) | byte_offset

    assert address >= 0 and address <= 0xFFFFFFFF, "Calculated address out of bounds: %s" % address
    return address


  def Validate(self, index):
    # Return 1 if address is a hit, 0 if miss
    return self.__cache[index][0]


  def Matching_Tags(self, index, tag):
    # Return 1 if tags match, 0 if not
    return self.__cache[index][1] == tag


  def Load_From_Memory(self, address):
    # Load data to cache from memory
    # TODO: How many words do I need to load?
    tag, index, word_offset = self.Address_Decode(address)
    word = self.__memory.Load_Word(address)
    self.__cache[index][2][word_offset] = word
    self.__cache[index][1] = tag
    self.__cache[index][0] = valid


  def Store_To_Memory(self, address, data):
    # Store data to memory from cache
    # TODO: How many words do I need to store?
    tag, index, word_offset = self.Address_Decode(address)
    word = self.__cache[index][2][word_offset]
    self.__memory.Store_Word(address, data)
    
    
  def Store(address, data):
    assert address >= 0 and address <= 0xFFFFFFFF, "Address out of bounds: %s" % address
    tag, index, word_offset = Address_Decode(address)

    # Cache miss
    if not Validate(index):
      self.Load_From_Memory(tag, index, word_offset)
      return "miss" # TODO: Probably also need to return number of cycles penalized

    # Need to evict
    if not Matching_Tags(index, tag):
      if self.Write_Policy == "back":
        # TODO: Should we do this always, or only when the block is dirty?
        evictee_tag = self.__cache[index][1]
        evictee_address = self.Encode_Address(
        # TODO: How many words/bytes to write back?
        self.Store_To_Memory(self, tag, index, word_offset, 0)
      # TODO: How many words do I load in?
      self.Load_From_Memory(tag, index, word_offset)
      # TODO: Do I return a fail status, or continue with the write?


    # Cache hit, write
    self.__cache[index][2][word_offset] = data
    if self.Write_Policy == "through":
      self.Store_To_Memory(address, data) # TODO: Do I need to use a buffer or something?


  def Load(address):
    assert address >= 0 and address <= 0xFFFFFFFF, "Address out of bounds: %s" % address
    tag, index, word_offset = Address_Decode(address)

    # Cache miss
    if not Validate(index):
      self.Load_From_Memory(tag, index, word_offset)
      return "miss" # TODO: Probably also need to return number of cycles penalized

    # Cache hit, fetch word
    return self.__cache[index][2][word_offset]



