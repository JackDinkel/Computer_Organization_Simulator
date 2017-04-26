import pipeline_reg
import hardware as HW
from control import *
from decode import *

#constants
INSTR_MEM_SIZE = 100
DATA_MEM_SIZE = 100

# pipeline registers
IFID  = pipeline_reg.IFID()
IDEX  = pipeline_reg.IDEX()
EXMEM = pipeline_reg.EXMEM()
MEMWB = pipeline_reg.MEMWB()

# state elements
PC = HW.PC()
Instruction_Memory = HW.Instruction_Memory(INSTR_MEM_SIZE)
Register_File = HW.Register_File()
Data_Memory = HW.Data_Memory(DATA_MEM_SIZE)

# non-register signals
WriteData = 0
PCSrc = 0

def pipelineMain():
	# initialize pc to zero
	IFID.pc_out = 0x00000000 

	# initialize some code
	Instruction_Memory.Store_Word(0,  0x21490001) # addi t1 t2 0x0001
	Instruction_Memory.Store_Word(4,  0x00000000) # nop
	Instruction_Memory.Store_Word(8,  0x00000000) # nop
	Instruction_Memory.Store_Word(12, 0x00000000) # nop
	Instruction_Memory.Store_Word(16, 0x00000000) # nop
	Instruction_Memory.Store_Word(16, 0x00000000) # nop

	# start pipeline
	for i in range(1,6):
		pipelineLoop()

	print "result: %d" % Register_File.Get(9)

def pipelineLoop():
	IF()
	WB()
	ID()
	EX()
	MEM()
	updateReg()

def IF():
	instruction_temp = Instruction()

	pc = HW.PC_Input_Mux(IFID.pc_out, EXMEM.branchAddress_out, EXMEM.jumpAddress_out, 
		PCSrc, EXMEM.memControl_out.Jump)

	instruction_temp.word = Instruction_Memory.Load_Word(pc)
	
	IFID.set(instruction_temp, pc+4)

def ID():
	# decode
	decodeInstruction(IFID.instruction_out)

	# combinatorial logic for control signals
	excTemp = EXControl()
	memcTemp = MEMControl()
	wbcTemp = WBControl()
	updateControl(IFID.instruction_out.op, IFID.instruction_out.funct, 
		excTemp, memcTemp, wbcTemp)

	print "RW: %d" % wbcTemp.RegWrite

	# Register file operations
	print "RegW: %d\n" % MEMWB.wbControl_out.RegWrite
	read_data_1, read_data_2 = Register_File.Operate(IFID.instruction_out.rs, 
		IFID.instruction_out.rt, MEMWB.destinationReg_out, WriteData, 
		MEMWB.wbControl_out.RegWrite)

	# inputs to IDEX register
	IDEX.set(IFID.instruction_out, HW.Sign_Extend(IFID.instruction_out.i_imm, 16), 
		IFID.pc_out, read_data_1, read_data_2, wbcTemp, memcTemp, excTemp)

def EX():
	# determine write reg address
	dest_reg_temp = HW.Register_Input_Mux(IDEX.instruction_out.rt, 
		IDEX.instruction_out.rd, IDEX.exControl_out.RegDst)

	# ALU
	alu_mux_temp = HW.ALU_Input_Mux(IDEX.readData2_out, IDEX.signExtendImm_out, 
		IDEX.exControl_out.ALUSrc)
	alu_res_temp = HW.ALU(IDEX.readData1_out, alu_mux_temp, IDEX.instruction_out.shamt, 
		IDEX.exControl_out.ALUOp)

	# calculate branch address
	branch_addr_temp = HW.Shift_Left_2(IDEX.signExtendImm_out) + IDEX.pc_out

	# calculate jump address
	jump_addr_temp = HW.Calculate_Jump_Addr(IDEX.instruction_out.j_imm, IDEX.pc_out)

	# inputs to EXMEM register
	EXMEM.set(IDEX.instruction_out, dest_reg_temp, IDEX.readData2_out, alu_res_temp, 
		(alu_res_temp == 0), branch_addr_temp, jump_addr_temp, IDEX.wbControl_out, 
		IDEX.memControl_out)

def MEM():
	global PCSrc
	PCSrc = 1 if (EXMEM.memControl_out.Branch == 1 and EXMEM.zero_out) else 0 # Python ternary operator

	# operate on data memory
	read_data_temp = Data_Memory.Operate(EXMEM.ALUResult_out, EXMEM.readData2_out, 
		EXMEM.memControl_out.MemRead, EXMEM.memControl_out.MemWrite, 
		EXMEM.instruction_out.op)

	# inputs to MEMWB register
	MEMWB.set(EXMEM.destinationReg_out, EXMEM.ALUResult_out, read_data_temp, 
		EXMEM.wbControl_out)

def WB():
	# update WriteData
	global WriteData
	WriteData = HW.Write_Back_Mux(MEMWB.readData_out, MEMWB.ALUResult_out, 
		MEMWB.wbControl_out.MemToReg)

def updateReg():
	IFID.update()
	IDEX.update()
	EXMEM.update()
	MEMWB.update()

if __name__ == "__main__":
	pipelineMain()