import pytest
import cache
from globals import *

def test_decode():
  c = cache.Direct_Cache(8, 1)
  assert c.Address_Decode(0b110110110) == (0b1101, 5, 0)

  c.Update(32, 2)
  assert c.Address_Decode(0b110110110) == (0b1, 0b10110, 1)

  c.Update(32, 4)
  assert c.Address_Decode(0b110110110) == (0, 0b11011, 01)
