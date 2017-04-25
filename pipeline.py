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
	
	IFID.set(if_instruction, pc+1)

def ID():
	return

def EX():
	return

def MEM():
	return

def WB():
	return

def updateReg():
	ifid.update()
	idex.update()
	exmem.update()
	memwb.update()

if __name__ == "__main__":
	main()