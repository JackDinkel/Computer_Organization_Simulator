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
	wbControl_in  = WBControl()
	memControl_in = MEMControl()
	exControl_in  = EXControl()

	# EX side
	instruction_out = Instruction()
	pc_out = 0
	wbControl_out  = WBControl()
	memControl_out = MEMControl()
	exControl_out  = EXControl()

	def set(this, i_in, p_in, wb_in, mem_in, ex_in):
		instruction_in = i_in
		pc_in = p_in
		wbControl_in = wb_in
		memControl_in = mem_in
		exControl_in = ex_in

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in
		wbControl_in = wbControl_out
		memControl_in = memControl_out
		exControl_in = exControl_out

class EXMEM:
	# EX side
	instruction_in = Instruction()
	pc_in = 0
	wbControl_in  = WBControl()
	memControl_in = MEMControl()

	# MEM side
	instruction_out = Instruction()
	pc_out = 0
	wbControl_out  = WBControl()
	memControl_out = MEMControl()

	def set(this, i_in, p_in, wb_in, mem_in):
		instruction_in = i_in
		pc_in = p_in
		wbControl_in = wb_in
		memControl_in = mem_in

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in
		wbControl_in = wbControl_out
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
		wbControl_in = wbControl_out
