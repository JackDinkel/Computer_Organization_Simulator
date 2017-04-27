import decode
from control import WBControl, MEMControl, EXControl

class IFID:
	# IF side
	instruction_in = decode.Instruction()
	pc_in = 0

	# ID side
	instruction_out = decode.Instruction()
	pc_out = 0

	stall = 0

	def set(self, i_in, p_in):
		self.instruction_in = i_in
		self.pc_in = p_in

	def flush(self):
		self.instruction_in.word = 0

	def update(self):
		if self.stall == 0:
			self.instruction_out = self.instruction_in
			self.pc_out = self.pc_in
		else:
			self.stall = 0

class IDEX:
	# ID side
	instruction_in = decode.Instruction()
	signExtendImm_in = 0
	pc_in = 0
	readData1_in = 0
	readData2_in = 0
	branchAddress_in = 0
	wbControl_in  = WBControl()
	memControl_in = MEMControl()
	exControl_in  = EXControl()

	# EX side
	instruction_out = decode.Instruction()
	signExtendImm_out = 0
	pc_out = 0
	readData1_out = 0
	readData2_out = 0
	branchAddress_out = 0
	wbControl_out  = WBControl()
	memControl_out = MEMControl()
	exControl_out  = EXControl()

	def set(self, i_in, sEx_in, p_in, rd1_in, rd2_in, b_in, wb_in, mem_in, ex_in):
		self.instruction_in = i_in
		self.signExtendImm_in = sEx_in
		self.pc_in = p_in
		self.readData1_in = rd1_in
		self.readData2_in = rd2_in
		self.branchAddress_in = b_in
		self.wbControl_in = wb_in
		self.memControl_in = mem_in
		self.exControl_in = ex_in

	def update(self):
		self.instruction_out = self.instruction_in
		self.signExtendImm_out = self.signExtendImm_in
		self.pc_out = self.pc_in
		self.readData1_out = self.readData1_in
		self.readData2_out = self.readData2_in
		self.branchAddress_out = self.branchAddress_in
		self.wbControl_out = self.wbControl_in
		self.memControl_out = self.memControl_in
		self.exControl_out = self.exControl_in

class EXMEM:
	# EX side
	instruction_in = decode.Instruction()
	destinationReg_in = 0
	readData2_in = 0
	ALUResult_in = 0
	zero_in = False
	jumpAddress_in = 0
	wbControl_in  = WBControl()
	memControl_in = MEMControl()

	# MEM side
	instruction_out = decode.Instruction()
	destinationReg_out = 0
	readData2_out = 0
	ALUResult_out = 0
	zero_out = False
	jumpAddress_out = 0
	wbControl_out  = WBControl()
	memControl_out = MEMControl()

	def set(self, i_in, destReg_in, rd2_in, aluR_in, z_in, jAdd_in, wbc_in, memc_in):
		self.instruction_in = i_in
		self.destinationReg_in = destReg_in
		self.readData2_in = rd2_in
		self.ALUResult_in = aluR_in
		self.zero_in = z_in
		self.jumpAddress_in = jAdd_in
		self.wbControl_in  = wbc_in
		self.memControl_in = memc_in

	def update(self):
		self.instruction_out = self.instruction_in
		self.destinationReg_out = self.destinationReg_in
		self.readData2_out = self.readData2_in
		self.ALUResult_out = self.ALUResult_in
		self.zero_out = self.zero_in
		self.jumpAddress_out = self.jumpAddress_in
		self.wbControl_out  = self.wbControl_in
		self.memControl_out = self.memControl_in

class MEMWB:
	# EX side
	destinationReg_in = 0
	ALUResult_in = 0
	readData_in = 0
	wbControl_in  = WBControl()

	# MEM side
	destinationReg_out = 0
	ALUResult_out = 0
	readData_out = 0
	wbControl_out  = WBControl()

	def set(self, dReg_in, aluR_in, rd_in, wb_in):
		self.destinationReg_in = dReg_in
		self.ALUResult_in = aluR_in
		self.readData_in = rd_in
		self.wbControl_in = wb_in

	def update(self):
		self.destinationReg_out = self.destinationReg_in
		self.ALUResult_out = self.ALUResult_in
		self.readData_out = self.readData_in
		self.wbControl_out  = self.wbControl_in
