import pytest
from pipeline import Pipeline
from register import REG_DICT

def test_forward():
	# init pipeline
	p = Pipeline()
	p.IFID.pc_out = 0

	# init instructions
	p.Instruction_Memory.Store_Word(0,  0x20090002) # addi t1 zero 0x0002
	p.Instruction_Memory.Store_Word(4,  0x200a0003) # addi t2 zero 0x0003
	p.Instruction_Memory.Store_Word(8,  0x200b0004) # addi t3 zero 0x0004
	p.Instruction_Memory.Store_Word(12, 0x200c0005) # addi t4 zero 0x0005
	p.Instruction_Memory.Store_Word(16, 0x012A4820) # add t1 t1 t2
	p.Instruction_Memory.Store_Word(20, 0x012B4820) # add t1 t1 t3
	p.Instruction_Memory.Store_Word(24, 0x012C4820) # add t1 t1 t4
	p.Instruction_Memory.Store_Word(28, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(32, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(36, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(40, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(44, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(48, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(52, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(56, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(60, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(64, 0x00000000) # nop
	p.Instruction_Memory.Store_Word(68, 0x00000000) # nop

	for i in range(1,15):
		p.pipelineLoop()

	assert p.Register_File.Get(REG_DICT["t1"]) == 14
	assert p.Register_File.Get(REG_DICT["t2"]) == 3
	assert p.Register_File.Get(REG_DICT["t3"]) == 4
	assert p.Register_File.Get(REG_DICT["t4"]) == 5
