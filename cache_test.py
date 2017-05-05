import pytest
import cache
from globals import *
import hardware as HW

def test_decode():
  c = cache.Direct_Cache(8, 1, "through", [], 0)
  assert c.Address_Decode(0b110110110) == (0b1101, 5, 0)

  c.Update(32, 2, "through", [], 0)
  assert c.Address_Decode(0b110110110) == (0b1, 0b10110, 1)

  c.Update(32, 4, "through", [], 0)
  assert c.Address_Decode(0b110110110) == (0, 0b11011, 01)

  c.Update(8, 2, "through", [], 0)
  assert c.Address_Decode(0b1011101001) == (11, 5, 0)

  c.Update(8, 4, "through", [], 0)
  assert c.Address_Decode(0b1011101001) == (5, 6, 2)


def test_encode():
  c = cache.Direct_Cache(8, 1, "through", [], 0)
  assert c.Address_Encode(0b1101, 5, 0, 0b10) == 0b110110110

  c.Update(32, 2, "through", [], 0)
  assert c.Address_Encode(1, 0b10110, 1, 2) == 0b110110110

  c.Update(32, 4, "through", [], 0)
  assert c.Address_Encode(0, 0b11011, 1, 2) == 0b110110110

  c.Update(8, 2, "through", [], 0)
  assert c.Address_Encode(11, 5, 0, 1) == 0b1011101001

  c.Update(8, 4, "through", [], 0)
  assert c. Address_Encode(5, 6, 2, 1) == 0b1011101001


def test_load_block_from_memory():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Load_Block_From_Memory(3) == range(2)
  assert c.Load_Block_From_Memory(26) == [6,7]

  
def test_store_block_to_memory():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Load_Block_From_Memory(3) == range(2)
  assert c.Load_Block_From_Memory(26) == [6,7]

  c.Direct_Update(0, [1, 0, [21, 22]]) #0b100000
  c.Direct_Update(3, [1, 0, [31, 32]])

  assert c.Store_Block_To_Memory(3)   == [21, 22]
  assert c.Store_Block_To_Memory(26)  == [31, 32]

  assert c.Load_Block_From_Memory(3)  == [21, 22]
  assert c.Load_Block_From_Memory(26) == [31, 32]

  mem = 32
  c.Update(8, 4, "through", range(mem), mem)

  assert c.Load_Block_From_Memory(3) == range(4)
  assert c.Load_Block_From_Memory(52) == [12,13,14,15]
  
  c.Direct_Update(0, [1, 0, [121, 122, 123, 124]]) #0b100000
  c.Direct_Update(3, [1, 0, [131, 132, 133, 134]])

  assert c.Store_Block_To_Memory(3)   == [121, 122, 123, 124]
  assert c.Store_Block_To_Memory(52)  == [131, 132, 133, 134]

  assert c.Load_Block_From_Memory(3)  == [121, 122, 123, 124]
  assert c.Load_Block_From_Memory(52) == [131, 132, 133, 134]

  mem = 32
  c.Update(8, 4, "through", range(mem), mem)

  assert c.Load_Block_From_Memory(7) == range(4)
  assert c.Load_Block_From_Memory(52) == [12,13,14,15]
  
  c.Direct_Update(0, [1, 0, [121, 122, 123, 124]]) #0b100000
  c.Direct_Update(3, [1, 0, [131, 132, 133, 134]])

  assert c.Store_Block_To_Memory(7)   == [121, 122, 123, 124]
  assert c.Store_Block_To_Memory(52)  == [131, 132, 133, 134]

  assert c.Load_Block_From_Memory(7)  == [121, 122, 123, 124]
  assert c.Load_Block_From_Memory(52) == [131, 132, 133, 134]


def test_tag():
  mem = 64
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Store(4, 0) == 'miss'
  for num in xrange(4):
    addr = (mem * num) + 4
    val = num * 1000
     
    assert c.Store(addr, val) == 'hit'
    assert c.Direct_Fetch(0) == [1, num, [(16 * num), val]]
    assert c.memory.Direct_Fetch(addr - 4) == 16 * num
    assert c.memory.Direct_Fetch(addr) == val


def test_store_through():
  mem = 32
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)

  assert c.Direct_Fetch(0) == [0, 0, [0, 0]]

  # This will miss, and pull from memory into the cache
  assert c.Store(2, 100) == 'miss'

  # Check that memory was properly pulled into the cache
  assert c.Direct_Fetch(0) == [1, 0, [0, 1]]

  # Try again, this will hit and store the word
  assert c.Store(2, 100) == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [100, 1]]

  # Check that it wrote through to memory
  assert c.memory.Direct_Fetch(0) == 100
  assert c.memory.Direct_Fetch(4) == 1

  # Try to store another word in the same block
  assert c.Store(4, 101) == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [100, 101]]
  assert c.memory.Direct_Fetch(0) == 100
  assert c.memory.Direct_Fetch(4) == 101

  # Store another word with a different tag in the same block - force an eviction
  assert c.Store(66, 200) != 'miss'
  assert c.Direct_Fetch(0) == [1, 1, [200, 17]]
  assert c.memory.Direct_Fetch(66) == 200
  assert c.memory.Direct_Fetch(68) == 17


def test_store_back():
  mem = 32
  c = cache.Direct_Cache(8, 2, "back", range(mem), mem)

  assert c.Direct_Fetch(0) == [0, 0, [0, 0]]

  # This will miss, and pull from memory into the cache
  assert c.Store(2, 100) == 'miss'

  # Check that memory was properly pulled into the cache
  assert c.Direct_Fetch(0) == [1, 0, [0, 1]]

  # Try again, this will hit and store the word
  assert c.Store(2, 100) == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [100, 1]]

  # Check that it did not write through to memory
  assert c.memory.Direct_Fetch(0) == 0
  assert c.memory.Direct_Fetch(4) == 1

  # Try to store another word in the same block
  assert c.Store(4, 101) == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [100, 101]]
  assert c.memory.Direct_Fetch(0) == 0
  assert c.memory.Direct_Fetch(4) == 1


  # Store another word with a different tag in the same block - force an eviction
  assert c.Store(66, 200) != 'miss'
  assert c.Direct_Fetch(0) == [1, 1, [200, 17]]
  assert c.memory.Direct_Fetch(66) == 16
  assert c.memory.Direct_Fetch(68) == 17

  # Check that it wrote back to memory
  assert c.memory.Direct_Fetch(0) == 100
  assert c.memory.Direct_Fetch(4) == 101


def test_load():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Load(3) == 'miss'
  assert c.Load(3) == 0
  assert c.Load(4) == 1
  assert c.Load(29) == 'miss'
  assert c.Load(24) == 6
  assert c.Load(29) == 7


def test_half():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Store(3, 0xffffffff) == 'miss'
  assert c.Store(3, 0xffffffff) == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0xffffffff, 1]]

  assert c.Store(0, 0x0811, 'h') == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0x0811ffff, 1]]

  assert c.Store(2, 0xf321, 'h') == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0x0811f321, 1]]

  assert c.Load(0) == HW.Sign_Extend(0x0811f321, 32)
  assert c.Load(0, 'hu') == 0x0811
  assert c.Load(2, 'hu') == 0xf321
  assert c.Load(0, 'h') == HW.Sign_Extend(0x0811, 16)
  assert c.Load(2, 'h') == HW.Sign_Extend(0xf321, 16)
  


def test_bytes():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Store(3, 0xffffffff) == 'miss'
  assert c.Store(3, 0xffffffff) == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0xffffffff, 1]]

  assert c.Store(0, 0x08, 'b') == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0x08ffffff, 1]]

  assert c.Store(2, 0x55, 'b') == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0x08ff55ff, 1]]

  assert c.Store(1, 0x21, 'b') == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0x082155ff, 1]]

  assert c.Store(3, 0x88, 'b') == 'hit'
  assert c.Direct_Fetch(0) == [1, 0, [0x08215588, 1]]

  assert c.Load(0) == HW.Sign_Extend(0x08215588, 32)
  assert c.Load(0, 'bu') == 0x08
  assert c.Load(1, 'bu') == 0x21
  assert c.Load(2, 'bu') == 0x55
  assert c.Load(3, 'bu') == 0x88
  assert c.Load(0, 'b') == HW.Sign_Extend(0x08, 8)
  assert c.Load(1, 'b') == HW.Sign_Extend(0x21, 8)
  assert c.Load(2, 'b') == HW.Sign_Extend(0x55, 8)
  assert c.Load(3, 'b') == HW.Sign_Extend(0x88, 8)

