import pytest
import cache
from globals import *

def test_decode():
  c = cache.Direct_Cache(8, 1, "through", [], 0)
  assert c.Address_Decode(0b110110110) == (0b1101, 5, 0)

  c.Update(32, 2, "through", [], 0)
  assert c.Address_Decode(0b110110110) == (0b1, 0b10110, 1)

  c.Update(32, 4, "through", [], 0)
  assert c.Address_Decode(0b110110110) == (0, 0b11011, 01)


def test_address_decode():
  c = cache.Direct_Cache(8, 2, "through", [], 0)
  assert c.Address_Decode(0b1011101001) == (5, 6, 2)


def test_address_encode():
  c = cache.Direct_Cache(8, 2, "through", [], 0)
  assert c.Address_Encode(5, 6, 2, 1) == 0b1011101001


def test_load_block():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Load_Block_From_Memory(3) == range(2)
  assert c.Load_Block_From_Memory(26) == [6,7]

  
def test_store_block():
  mem = 16
  c = cache.Direct_Cache(8, 2, "through", range(mem), mem)
  assert c.Load_Block_From_Memory(3) == range(2)
  assert c.Load_Block_From_Memory(26) == [6,7]

  c.Direct_Update(0, [1, 0, [21, 22]]) #0b100000
  c.Direct_Update(3, [1, 0, [31, 32]])

  c.display()
  c.memory.display()

  assert c.Store_Block_To_Memory(3)   == [21, 22]
  assert c.Store_Block_To_Memory(26)  == [31, 32]

  c.display()
  c.memory.display()

  assert c.Load_Block_From_Memory(3)  == [21, 22]
  assert c.Load_Block_From_Memory(26) == [31, 32]
