from decode import Decoder as Instruction
from control import Controller

class IFID:
	instruction_in = Instruction()
	instruction_out = Instruction()
	pc_in = 0
	pc_out = 0

	def set(this, i_in, p_in):
		instruction_in = i_in
		pc_in = p_in

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in

class IDEX:

	pc_in = 0
	pc_out = 0

	def set_instruction(this, i_in):
		instruction_in = i_in

	def set_pc(this, p_in):
		pc_in = p_in

	def get_instruction(this):
		return instruction_out

	def get_pc(this):
		return pc_out

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in

class EXMEM:
	instruction_in = Instruction()
	instruction_out = Instruction()
	pc_in = 0
	pc_out = 0

	def set_instruction(this, i_in):
		instruction_in = i_in

	def set_pc(this, p_in):
		pc_in = p_in

	def get_instruction(this):
		return instruction_out

	def get_pc(this):
		return pc_out

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in

class MEMWB:
	instruction_in = Instruction()
	instruction_out = Instruction()
	pc_in = 0
	pc_out = 0

	def set_instruction(this, i_in):
		instruction_in = i_in

	def set_pc(this, p_in):
		pc_in = p_in

	def get_instruction(this):
		return instruction_out

	def get_pc(this):
		return pc_out

	def update(this):
		instruction_out = instruction_in
		pc_out = pc_in