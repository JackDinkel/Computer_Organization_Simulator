import pipeline_reg
import hardware as HW
from decode import Decoder as Instruction

# pipeline registers
IFID  = pipeline_reg.IFID()
IDEX  = pipeline_reg.IDEX()
EXMEM = pipeline_reg.EXMEM()
MEMWB = pipeline_reg.MEMWB()

# state elements
PC = HW.PC()
Instruction_Memory = HW.Instruction_Memory()
Register_File = HW.Register_File()
Data_Memory = HW.Data_Memory()

# non-register signals
WriteData = 0

def main():
	# start pipeline
	pipelineLoop()

def pipelineLoop():
	IF()
	WB()
	ID()
	EX()
	MEM()
	updateReg()

def IF():
	if_instruction = Instruction()
	pc = PC.Get()

	if_instruction.word = Instruction_Memory.Fetch_Word(pc)
	
	IFID.set(if_instruction, pc+4)

def ID():
	# decode
	decodeInstruction(IFID.instruction_out)

	# combinatorial logic for control signals
	excTemp = EXControl()
	memcTemp = MEMControl()
	wbcTemp = WBControl()
	updateControl(IFID.instruction_out.op, IFID.instruction_out.funct, 
		excTemp, memcTemp, wbcTemp)

	# Register file operations
	read_data_1, read_data_2 = Register_File.Operate(IFID.instruction_out.rs, 
		IFID.instruction_out.rt, MEMWB.writeReg_out, WriteData, 
		MEMWB.wbControl_out.RegWrite)

	# inputs to IDEX register
	IDEX.set(IFID.instruction_out, IFID.pc_out, read_data_1, read_data_2, 
		wbcTemp, memcTemp, excTemp)

def EX():
	# determine write reg address
	dest_reg_temp = Register_Input_Mux(IDEX.instruction_out.rt, 
		IDEX.instruction_out.rd, IDEX.exControl_out.RegDst)

	# ALU
	alu_mux_temp = ALU_Input_Mux(IDEX.readData2_out, IDEX.instruction_out.i_imm, #TODO: need to sign-extend immed?
		IDEX.exControl_out.ALUSrc)
	alu_res_temp = ALU(IDEX.readData1_out, alu_mux_temp, IDEX.instruction_out.shamt, 
		IDEX.exControl_out.ALUOp)

	# calculate branch address
	branch_addr_temp = Shift_Left_2(IDEX.instruction_out.i_imm) + IDEX.pc_out

	EXMEM.set(dest_reg_temp, IDEX.readData2_out, alu_res_temp, (alu_res_temp == 0), 
		branch_addr_temp, IDEX.wbControl_out, IDEX.memControl_out)
	return

def MEM():
	return

def WB():
	# update WriteData
	return

def updateReg():
	ifid.update()
	idex.update()
	exmem.update()
	memwb.update()

if __name__ == "__main__":
	main()