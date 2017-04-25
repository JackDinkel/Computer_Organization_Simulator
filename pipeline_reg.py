import decode
import control

class IFID:
	# IF side
	instruction_in = Instruction()
	pc_in = 0

	# ID side
	instruction_out = Instruction()
	pc_out = 0

	def set(this, i_in, p_in):
		instruction_in = i_in
		pc_in = p_in

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in

class IDEX:
	# ID side
	instruction_in = Instruction()
	pc_in = 0
	readData1_in = 0
	readData2_in = 0
	wbControl_in  = WBControl()
	memControl_in = MEMControl()
	exControl_in  = EXControl()

	# EX side
	instruction_out = Instruction()
	pc_out = 0
	readData1_out = 0
	readData2_out = 0
	wbControl_out  = WBControl()
	memControl_out = MEMControl()
	exControl_out  = EXControl()

	def set(this, i_in, p_in, rd1_in, rd2_in, wb_in, mem_in, ex_in):
		instruction_in = i_in
		pc_in = p_in
		readData1_in = rd1_in
		readData2_in = rd2_in
		wbControl_in = wb_in
		memControl_in = mem_in
		exControl_in = ex_in

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in
		readData1_out = readData1_in
		readData2_out = readData2_in
		wbControl_out = wbControl_in
		memControl_out = memControl_in
		exControl_out = exControl_in

class EXMEM:
	# EX side
	destinationReg_in = 0
	readData2_in = 0
	ALUResult_in = 0
	zero_in = False
	branchAddress_in = 0
	wbControl_in  = WBControl()
	memControl_in = MEMControl()

	# MEM side
	destinationReg_out = 0
	readData2_out = 0
	ALUResult_out = 0
	zero_out = False
	branchAddress_out = 0
	wbControl_out  = WBControl()
	memControl_out = MEMControl()

	def set(this, destReg_in, rd2_in, aluR_in, z_in, bAdd_in, wbc_in, memc_in):
		destinationReg_in = destReg_in
		readData2_in = rd2_in
		ALUResult_in = aluR_in
		zero_in = z_in
		branchAddress_in = bAdd_in
		wbControl_in  = wbc_in
		memControl_in = memc_in

	def update(this):
		destinationReg_in = destinationReg_out
		readData2_in = readData2_out
		ALUResult_in = ALUResult_out
		zero_in = zero_out
		branchAddress_in = branchAddress_out
		wbControl_in  = wbControl_out
		memControl_in = memControl_out

class MEMWB:
	# EX side
	instruction_in = Instruction()
	pc_in = 0
	wbControl_in  = WBControl()

	# MEM side
	instruction_out = Instruction()
	pc_out = 0
	wbControl_out  = WBControl()

	def set(this, i_in, p_in, wb_in):
		instruction_in = i_in
		pc_in = p_in
		wbControl_in = wb_in

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in
		wbControl_out = wbControl_in
