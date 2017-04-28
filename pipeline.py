import pipeline_reg
import hardware as HW
from register import REG_DICT
from opcode import *
from control import *
from decode import *

#constants
MEM_SIZE = 400

def pipelineMain():
	p = Pipeline()

	# initialize pc to zero
	p.IFID.pc_out = 0x00000000 

	# initialize some code
	p.Memory.Store_Word(0,  0x2008000F) # addi t0 zero 0xF
	p.Memory.Store_Word(4,  0x20090005) # addi t1 zero 0x5
	p.Memory.Store_Word(8,  0x312A0001) # andi t2 t1 0x1 <-- bug due to no forwarding
	p.Memory.Store_Word(12, 0x392B0003) # xori t3 t1 0x3
	p.Memory.Store_Word(16, 0x350C0003) # ori  t4 t0 0x3
	p.Memory.Store_Word(20, 0x292D000F) # slti t5 t1 0xF
	p.Memory.Store_Word(24, 0x00000000) # nop
	p.Memory.Store_Word(28, 0x00000000) # nop
	p.Memory.Store_Word(32, 0x00000000) # nop
	p.Memory.Store_Word(36, 0x00000000) # nop
	p.Memory.Store_Word(40, 0x00000000) # nop
	p.Memory.Store_Word(44, 0x00000000) # nop
	p.Memory.Store_Word(48, 0x00000000) # nop
	p.Memory.Store_Word(52, 0x00000000) # nop
	p.Memory.Store_Word(56, 0x00000000) # nop
	p.Memory.Store_Word(60, 0x00000000) # nop
	p.Memory.Store_Word(64, 0x00000000) # nop
	p.Memory.Store_Word(68, 0x00000000) # nop

	# start pipeline
	for i in range(1,20):
		p.pipelineLoop()

	print "\nt0: %d" % p.Register_File.Get(REG_DICT["t0"])
	print "t1: %d" % p.Register_File.Get(REG_DICT["t1"])
	print "t2: %d" % p.Register_File.Get(REG_DICT["t2"])
	print "t3: %d" % p.Register_File.Get(REG_DICT["t3"])
	print "t4: %d" % p.Register_File.Get(REG_DICT["t4"])
	print "t5: %d" % p.Register_File.Get(REG_DICT["t5"])
	print "t6: %d" % p.Register_File.Get(REG_DICT["t6"])
	print "t7: %d" % p.Register_File.Get(REG_DICT["t7"])
	print "t8: %d" % p.Register_File.Get(REG_DICT["t8"])
	print "t9: %d" % p.Register_File.Get(REG_DICT["t9"])
	print "ra: %d" % p.Register_File.Get(REG_DICT["ra"])

class Pipeline(object):
	# pipeline registers
	IFID  = pipeline_reg.IFID()
	IDEX  = pipeline_reg.IDEX()
	EXMEM = pipeline_reg.EXMEM()
	MEMWB = pipeline_reg.MEMWB()

	# state elements
	PC = HW.PC()
	Memory = HW.Memory([], MEM_SIZE)
	Register_File = HW.Register_File()

	# non-register signals
	WriteData = 0
	PCSrc = 0
	PCSrcJ = 0

	def pipelineLoop(self):
		self.IF()
		self.WB()
		self.ID()
		self.EX()
		self.MEM()
		self.updateReg()

	def IF(self):
		instruction_temp = Instruction()

		pc = HW.PC_Input_Mux(self.IFID.pc_out, self.IDEX.branchAddress_out, self.IDEX.jumpAddress_out, 
			self.PCSrc, self.PCSrcJ)

		instruction_temp.word = self.Memory.Instruction_Operate(pc, 0, 1, 0)

		print "%d, %d" % (pc, instruction_temp.word)

		self.IFID.set(instruction_temp, pc+4)

	def ID(self):
		# decode
		decodeInstruction(self.IFID.instruction_out)

		# combinatorial logic for control signals
		excTemp = EXControl()
		memcTemp = MEMControl()
		wbcTemp = WBControl()
		updateControl(self.IFID.instruction_out.op, self.IFID.instruction_out.funct, 
			excTemp, memcTemp, wbcTemp)

		# find dest register
		dest_reg_temp = HW.Register_Input_Mux(self.IFID.instruction_out.rt, 
			self.IFID.instruction_out.rd, excTemp.RegDst)

		# sign extend immediate
		sign_extend_imm = HW.Sign_Extend(self.IFID.instruction_out.i_imm, 16)

		#branch forwarding
		if (self.EXMEM.wbControl_out.RegWrite and (self.EXMEM.destinationReg_out == self.IFID.instruction_out.rs)):
			rs_value = self.EXMEM.ALUResult_out
		elif (self.MEMWB.wbControl_out.RegWrite and (self.MEMWB.destinationReg_out == self.IFID.instruction_out.rs)):
			rs_value = self.WriteData
		else:
			rs_value = self.Register_File.Get(self.IFID.instruction_out.rs)

		if (self.EXMEM.wbControl_out.RegWrite and (self.EXMEM.destinationReg_out == self.IFID.instruction_out.rt)):
			rt_value = self.EXMEM.ALUResult_out
		elif (self.MEMWB.wbControl_out.RegWrite and (self.MEMWB.destinationReg_out == self.IFID.instruction_out.rt)):
			rt_value = self.WriteData
		else:
			rt_value = self.Register_File.Get(self.IFID.instruction_out.rt)

		# branch hazards
		if ((self.IFID.instruction_out.op == OP_DICT["BEQ"] or 
			self.IFID.instruction_out.op == OP_DICT["BNE"]) and 
		(((self.EXMEM.memControl_out.MemRead == 1) and 
			((self.EXMEM.destinationReg_out == self.IFID.instruction_out.rt) 
				or (self.EXMEM.destinationReg_out == self.IFID.instruction_out.rs))) or 
		(((self.IDEX.memControl_out.MemRead == 1) or (self.IDEX.instruction_out.op == 0)) and 
			((self.IDEX.destinationReg_out == self.IFID.instruction_out.rt) 
				or (self.IDEX.destinationReg_out == self.IFID.instruction_out.rs))) or
		((self.IDEX.instruction_out.op > 3 and self.IDEX.instruction_out.op != OP_DICT["BEQ"] and
		 self.IDEX.instruction_out.op != OP_DICT["BNE"]) and (self.IDEX.memControl_out.MemWrite == 0) 
			and (self.IDEX.destinationReg_out == self.IFID.instruction_out.rt)))):
			HW.Hazard_Detection_Mux(excTemp, memcTemp, wbcTemp, 1)
			self.IFID.stall = 1
		else:
			# branch detection
			if (((self.IFID.instruction_out.op == OP_DICT["BEQ"]) and (rs_value == rt_value)) 
				or ((self.IFID.instruction_out.op == OP_DICT["BNE"]) and (rs_value != rt_value))):
				self.IFID.flush()
				self.PCSrc = 1
			else:
				self.PCSrc = 0

		# hazard detection
		data_hazard = HW.Hazard_Detection_Unit(self.IDEX.memControl_out.MemRead, self.IDEX.instruction_out.rt, 
			self.IFID.instruction_out.rs, self.IFID.instruction_out.rt)
		HW.Hazard_Detection_Mux(excTemp, memcTemp, wbcTemp, data_hazard)
		if data_hazard == 1:
			self.IFID.stall = 1

		# calculate branch address
		branch_addr_temp = HW.Shift_Left_2(sign_extend_imm) + self.IFID.pc_out

		# jump detection
		if ((self.IFID.instruction_out.op == OP_DICT["J"]) or 
			(self.IFID.instruction_out.op == OP_DICT["JAL"])):
			self.IFID.flush()
			self.PCSrcJ = 1
			if self.IFID.instruction_out.op == OP_DICT["JAL"]:
				self.Register_File.Set(REG_DICT["ra"], self.IFID.pc_out + 4)
		else:
			self.PCSrcJ = 0

		# calculate jump address
		jump_addr_temp = HW.Calculate_Jump_Addr(self.IFID.instruction_out.j_imm, self.IFID.pc_out)

		# Register file operations
		read_data_1, read_data_2 = self.Register_File.Operate(self.IFID.instruction_out.rs, 
			self.IFID.instruction_out.rt, self.MEMWB.destinationReg_out, self.WriteData, 
			self.MEMWB.wbControl_out.RegWrite)

		# inputs to IDEX register
		self.IDEX.set(self.IFID.instruction_out, dest_reg_temp, sign_extend_imm, self.IFID.pc_out, 
			read_data_1, read_data_2, branch_addr_temp, jump_addr_temp, wbcTemp, memcTemp, excTemp)

	def EX(self):
		# Forwarding
		(forwardA, forwardB) = HW.Forwarding_Unit(self.IDEX.instruction_out.rs, self.IDEX.instruction_out.rt, 
			self.EXMEM.instruction_out.rd, self.MEMWB.destinationReg_out, self.EXMEM.wbControl_out.RegWrite, 
			self.MEMWB.wbControl_out.RegWrite)

		# ALU
		alu_input_1 = HW.ALU_Reg_A_Mux(self.IDEX.readData1_out, self.WriteData, self.EXMEM.ALUResult_out, forwardA)
		alu_input_2 = HW.ALU_Reg_B_MUX(self.IDEX.readData2_out, self.WriteData, self.EXMEM.ALUResult_out, forwardB)
		alu_mux_temp = HW.ALU_Input_Mux2(alu_input_2, self.IDEX.signExtendImm_out, 
			self.IDEX.exControl_out.ALUSrc)
		alu_res_temp, dc1, dc2 = HW.ALU(alu_input_1, alu_mux_temp, self.IDEX.instruction_out.shamt, 
			self.IDEX.exControl_out.ALUOp)

		# inputs to EXMEM register
		self.EXMEM.set(self.IDEX.instruction_out, self.IDEX.destinationReg_out, self.IDEX.readData2_out, 
			alu_res_temp, (alu_res_temp == 0), self.IDEX.wbControl_out, 
			self.IDEX.memControl_out)

	def MEM(self):
		# operate on data memory
		read_data_temp = self.Memory.Data_Operate(self.EXMEM.ALUResult_out, self.EXMEM.readData2_out, 
			self.EXMEM.memControl_out.MemRead, self.EXMEM.memControl_out.MemWrite, 
			self.EXMEM.instruction_out.op)

		# inputs to MEMWB register
		self.MEMWB.set(self.EXMEM.destinationReg_out, self.EXMEM.ALUResult_out, read_data_temp, 
			self.EXMEM.wbControl_out)

	def WB(self):
		# update WriteData
		self.WriteData = HW.Write_Back_Mux(self.MEMWB.readData_out, self.MEMWB.ALUResult_out, 
			self.MEMWB.wbControl_out.MemToReg)

	def updateReg(self):
		self.IFID.update()
		self.IDEX.update()
		self.EXMEM.update()
		self.MEMWB.update()

if __name__ == "__main__":
	pipelineMain()