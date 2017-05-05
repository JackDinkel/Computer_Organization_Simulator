import hardware as HW
import decode
import pytest
import mask
from control import ALU_DICT
from register import REG_DICT
import cache
from globals import *
import memory
import memory_init



###### Hardware ###################################
def test_twos_comp():
  val1 = 0
  val2 = 11
  val3 = -16
  val4 = 0xFFFFFFF0

  assert HW.twos_comp(val1, 32) == val1
  assert HW.twos_comp(val2, 32) == val2
  assert HW.twos_comp(val3, 32) == val3
  assert HW.twos_comp(val4, 32) == val3

  assert HW.unsigned(val1, 32) == val1
  assert HW.unsigned(val2, 32) == val2
  assert HW.unsigned(val3, 32) == val4
  assert HW.unsigned(val4, 32) == val4


def test_mux():
  assert HW.MUX("hi", 123, 0) == "hi"
  assert HW.MUX("hi", 123, 1) == 123


def test_PC():
  v = 0
  mypc = HW.PC()
  assert mypc.Get() == v

  v = 400
  mypc.Set(v)
  assert mypc.Get() == v


def test_Instruction_Decode():
  decoder = decode.Instruction

  decoder.word = 0x00000000
  decode.decodeInstruction(decoder)
  assert decoder.op == 0x0
  assert decoder.rs == 0x0
  assert decoder.rt == 0x0
  assert decoder.rd == 0x0
  assert decoder.shamt == 0x0
  assert decoder.funct == 0x0
  assert decoder.i_imm == 0x0
  assert decoder.j_imm == 0x0

  # subu t4,t5,t3
  decoder.word = 0x01ab6023 
  decode.decodeInstruction(decoder)
  assert decoder.op == 0x0
  assert decoder.rs == 0xD
  assert decoder.rt == 0xB
  assert decoder.rd == 0xC
  assert decoder.shamt == 0x0
  assert decoder.funct == 0x23

  # addiu t5,a1,-1
  decoder.word = 0x24adffff 
  decode.decodeInstruction(decoder)
  assert decoder.op == 0x9
  assert decoder.rs == 0x5
  assert decoder.rt == 0xD
  assert decoder.i_imm == 0xFFFF

  # jal 120
  decoder.word = 0x0c000078 
  decode.decodeInstruction(decoder)
  assert decoder.op == 0x3
  assert decoder.j_imm == 0x78


def test_Register_File():
  f = HW.Register_File()

  a1 = REG_DICT["a1"]
  t1 = REG_DICT["t1"]
  value = 0x100
  RegWriteOn = 1
  RegWriteOff = 0

  # Check if a1 and t1 are zero
  assert f.Operate(a1, t1, t1, value, RegWriteOff) == (0, 0)
  assert f.Get(a1) == 0
  assert f.Get(t1) == 0

  # Load 0x100 into t1
  # Check that a1 is 0 and t1 is 0x100
  assert f.Operate(a1, t1, t1, value, RegWriteOn) == (0, value)
  assert f.Get(a1) == 0
  assert f.Get(t1) == value

  # Check that a1 is 0 and t1 is 0x100
  assert f.Operate(a1, t1, t1, value, RegWriteOff) == (0, value)
  assert f.Get(a1) == 0
  assert f.Get(t1) == value


def test_Sign_Extend():
  val1 = 0b1111111111110000 # -16
  val2 = 0xFFFF # -1
  val3 = 0xFFCE # -50
  val4 = 0x0064 # 100
  val5 = 0x0000 # 0

  assert HW.Sign_Extend(val1, 16) == 0b11111111111111111111111111110000
  assert HW.Sign_Extend(val2, 16) == 0b11111111111111111111111111111111
  assert HW.Sign_Extend(val3, 16) == 0b11111111111111111111111111001110
  assert HW.Sign_Extend(val4, 16) == 0b00000000000000000000000001100100
  assert HW.Sign_Extend(val5, 16) == 0b00000000000000000000000000000000


def test_get_byte():
  num = 0x12345678
  assert mask.Get_Byte(num, 0) == 0x12
  assert mask.Get_Byte(num, 1) == 0x34
  assert mask.Get_Byte(num, 2) == 0x56
  assert mask.Get_Byte(num, 3) == 0x78
  assert mask.Get_Half(num, 0) == 0x1234
  assert mask.Get_Half(num, 2) == 0x5678


def test_ALU():
  #TODO
  input1 = 5
  input2 = 2
  shamt = 3

  #assert HW.ALU(input1, input2, 0, ALU_DICT["X"])     == (0, 0) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["AND"])   == (input1 & input2, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["OR"])    == (input1 | input2, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["ADD"])   == (input1 + input2, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["ADDU"])  == (input1 + input2, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SUB"])   == (input1 - input2, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SUBU"])  == (input1 - input2, 0, 0)
  assert HW.ALU(input1, input2,shamt,ALU_DICT["SLL"]) == (input2 << shamt, 0, 0)
  assert HW.ALU(input1, input2,shamt,ALU_DICT["SRL"]) == (input2 >> shamt, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SLT"])   == (0, 0, 1) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["SLTU"])  == (0, 0, 1) # TODO
  assert HW.ALU(input1, input2, 0, ALU_DICT["NOT"])   == (~input1, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["LW"])    == (7, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["LBU"])   == (7, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["LHU"])   == (7, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SW"])    == (7, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SH"])    == (7, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["SB"])    == (7, 0, 0)
  assert HW.ALU(input1, input2, 0, ALU_DICT["NOR"])   == (~(input1 | input2), 0, 0) # TODO


######## Memory/Cache #####################################################

def test_memory():
  size = 32
  mem = memory.Memory(size, range(size))
  mem.Store(8, 0xf2345688)
  assert mem.Load(8)        == 0xf2345688
  assert mem.Load(8,  'h')  == HW.Sign_Extend(0xf234, 16)
  assert mem.Load(10, 'h')  == HW.Sign_Extend(0x5688, 16)
  assert mem.Load(8,  'hu') == 0xf234
  assert mem.Load(10, 'hu') == 0x5688
  assert mem.Load(8,  'b')  == HW.Sign_Extend(0xf2, 8)
  assert mem.Load(9,  'b')  == HW.Sign_Extend(0x34, 8)
  assert mem.Load(10, 'b')  == HW.Sign_Extend(0x56, 8)
  assert mem.Load(11, 'b')  == HW.Sign_Extend(0x88, 8)
  assert mem.Load(8,  'bu') == 0xf2
  assert mem.Load(9,  'bu') == 0x34
  assert mem.Load(10, 'bu') == 0x56
  assert mem.Load(11, 'bu') == 0x88

  mem.Store(10, 0xcc, 'b')
  assert mem.Load(8) == 0xf234cc88
  assert mem.Load(10, 'bu') == 0xcc

  mem.Store(10, 0xaaaa, 'h')
  assert mem.Load(8) == 0xf234aaaa
  assert mem.Load(10, 'hu') == 0xaaaa


def test_cache_address_decode():
  mem = memory.Memory(0)
  c = cache.Direct_Cache(8, 1, "through", mem)
  assert c.Address_Decode(0b110110110) == (0b1101, 5, 0)

  c.Update(32, 2, "through", mem)
  assert c.Address_Decode(0b110110110) == (0b1, 0b10110, 1)

  c.Update(32, 4, "through", mem)
  assert c.Address_Decode(0b110110110) == (0, 0b11011, 01)

  c.Update(8, 2, "through", mem)
  assert c.Address_Decode(0b1011101001) == (11, 5, 0)

  c.Update(8, 4, "through", mem)
  assert c.Address_Decode(0b1011101001) == (5, 6, 2)


def test_cache_address_encode():
  mem = memory.Memory(0)
  c = cache.Direct_Cache(8, 1, "through", mem)
  assert c.Address_Encode(0b1101, 5, 0, 0b10) == 0b110110110

  c.Update(32, 2, "through", mem)
  assert c.Address_Encode(1, 0b10110, 1, 2) == 0b110110110

  c.Update(32, 4, "through", mem)
  assert c.Address_Encode(0, 0b11011, 1, 2) == 0b110110110

  c.Update(8, 2, "through", mem)
  assert c.Address_Encode(11, 5, 0, 1) == 0b1011101001

  c.Update(8, 4, "through", mem)
  assert c. Address_Encode(5, 6, 2, 1) == 0b1011101001


def test_cache_load_block_from_memory():
  mem = memory.Memory(16, range(16))
  c = cache.Direct_Cache(8, 2, "through", mem)
  assert c.Load_Block_From_Memory(3) == range(2)
  assert c.Load_Block_From_Memory(26) == [6,7]

  
def test_cache_store_block_to_memory():
  mem = memory.Memory(16, range(16))
  c = cache.Direct_Cache(8, 2, "through", mem)
  assert c.Load_Block_From_Memory(3) == range(2)
  assert c.Load_Block_From_Memory(26) == [6,7]

  c.Direct_Update(0, [1, 0, [21, 22]]) #0b100000
  c.Direct_Update(3, [1, 0, [31, 32]])

  assert c.Store_Block_To_Memory(3)   == [21, 22]
  assert c.Store_Block_To_Memory(26)  == [31, 32]

  assert c.Load_Block_From_Memory(3)  == [21, 22]
  assert c.Load_Block_From_Memory(26) == [31, 32]

  mem.Update(32, range(32))
  c = cache.Direct_Cache(8, 4, "through", mem)

  assert c.Load_Block_From_Memory(3) == range(4)
  assert c.Load_Block_From_Memory(52) == [12,13,14,15]
  
  c.Direct_Update(0, [1, 0, [121, 122, 123, 124]]) #0b100000
  c.Direct_Update(3, [1, 0, [131, 132, 133, 134]])

  assert c.Store_Block_To_Memory(3)   == [121, 122, 123, 124]
  assert c.Store_Block_To_Memory(52)  == [131, 132, 133, 134]

  assert c.Load_Block_From_Memory(3)  == [121, 122, 123, 124]
  assert c.Load_Block_From_Memory(52) == [131, 132, 133, 134]

  mem.Update(32, range(32))
  c.Update(8, 4, "through", mem)

  assert c.Load_Block_From_Memory(7) == range(4)
  assert c.Load_Block_From_Memory(52) == [12,13,14,15]
  
  c.Direct_Update(0, [1, 0, [121, 122, 123, 124]]) #0b100000
  c.Direct_Update(3, [1, 0, [131, 132, 133, 134]])

  assert c.Store_Block_To_Memory(7)   == [121, 122, 123, 124]
  assert c.Store_Block_To_Memory(52)  == [131, 132, 133, 134]

  assert c.Load_Block_From_Memory(7)  == [121, 122, 123, 124]
  assert c.Load_Block_From_Memory(52) == [131, 132, 133, 134]


def test_cache_tag():
  mem = memory.Memory(64, range(64))
  c = cache.Direct_Cache(8, 2, "through", mem)
  assert c.Store(4, 0) == 'miss'
  for num in xrange(4):
    addr = (64 * num) + 4
    val = num * 1000
     
    assert c.Store(addr, val) == 'hit'
    assert c.Direct_Fetch(0) == [1, num, [(16 * num), val]]
    assert c.memory.Direct_Fetch(addr - 4) == 16 * num
    assert c.memory.Direct_Fetch(addr) == val


def test_cache_store_through():
  mem = memory.Memory(32, range(32))
  c = cache.Direct_Cache(8, 2, "through", mem)

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


def test_cache_store_back():
  mem = memory.Memory(32, range(32))
  c = cache.Direct_Cache(8, 2, "back", mem)

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


def test_cache_load():
  mem = memory.Memory(16, range(16))
  c = cache.Direct_Cache(8, 2, "through", mem)
  assert c.Load(3) == 'miss'
  assert c.Load(3) == 0
  assert c.Load(4) == 1
  assert c.Load(29) == 'miss'
  assert c.Load(24) == 6
  assert c.Load(29) == 7


def test_cache_half():
  mem = memory.Memory(16, range(16))
  c = cache.Direct_Cache(8, 2, "through", mem)
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
  


def test_cache_bytes():
  mem = memory.Memory(16, range(16))
  c = cache.Direct_Cache(8, 2, "through", mem)
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


def test_cache_scheme():
  mem = memory_init.memory("direct", "through", 8, 2, 8, 2, 100)

