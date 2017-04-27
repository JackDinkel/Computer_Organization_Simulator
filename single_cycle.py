import hardware as HW
import decode
from control import Controller
from register import *

class Single_Cycle(object):
  mem_size = 1200

  # Initialize helpers
  decoder    = decode.Decoder()
  controller = Controller()
  
  
  # Initialize hardware
  PC = HW.PC()
  Register_File = HW.Register_File()


  # Initialize variables
  write_back = 0
  incremented_pc = 0
  branch_addr = 0
  jump_addr = 0
  j_enable = 0
  do_jump = False
  FIRST_CYCLE = True
  PROGRAM_EXIT = False
  delayed_branch = False
  delayed_branch_pc = 0

  def __init__(self, program):
    self.memory = HW.Memory(program, self.mem_size)


  def cycle(self):
   
    ### Execute ###
    # Instruction Fetch
    next_pc = HW.PC_Input_Mux(self.incremented_pc, self.branch_addr, self.jump_addr, (self.controller.Branch & self.j_enable), self.controller.Jump)

    if self.delayed_branch:
      next_pc = self.delayed_branch_pc
      self.delayed_branch = False
    if self.controller.Branch or self.controller.Jump:
      self.delayed_branch = True
      print "Taking a branch"
      self.delayed_branch_pc = next_pc
      next_pc = self.PC.Get() + 8

    if next_pc == 0 and not self.FIRST_CYCLE:
      self.PROGRAM_EXIT = True
    if not self.FIRST_CYCLE:
      self.PC.Set(next_pc)
    self.FIRST_CYCLE = False

    current_pc = self.PC.Get()
    current_instr = self.memory.Instruction_Operate(current_pc, 0, 1, 0)  
    print "Executing instruction", hex(current_instr)
    self.incremented_pc = HW.Add_Four(current_pc)
    
    # Instruction Decode and Register File Read
    self.decoder.decode(current_instr)
    self.controller.update(self.decoder.op, self.decoder.funct)
    write_reg = HW.Register_Input_Mux(self.decoder.rt, self.decoder.rd, self.controller.RegDst) 

    # Register Read
    read_data_1, read_data_2 = self.Register_File.Operate(self.decoder.rs, self.decoder.rt, write_reg, self.write_back, 0)
    
    # Execute and Adress Calculation
    extended_i_imm = HW.Sign_Extend(self.decoder.i_imm, 16)
    alu_operand_1 = HW.ALU_Input_Mux1(read_data_1, read_data_2, self.controller.ALUSrc1)
    alu_operand_2 = HW.ALU_Input_Mux2(read_data_2, extended_i_imm, self.controller.ALUSrc2)
    a = HW.ALU(alu_operand_1, alu_operand_2, self.decoder.shamt, self.controller.ALUOp)
    alu_result, self.j_enable, alu_reg_set = HW.ALU(alu_operand_1, alu_operand_2, self.decoder.shamt, self.controller.ALUOp)
    if alu_result == "pc":
      alu_result = PC.Get() + 8
    else:
      alu_result = HW.twos_comp(alu_result, 32)
    shifted_i_imm = HW.Shift_Left_2(HW.twos_comp(extended_i_imm, 32))
    self.branch_addr = HW.Address_Adder(self.incremented_pc, shifted_i_imm)
    self.jump_addr = HW.Calculate_Jump_Addr(self.decoder.j_imm, self.incremented_pc)
    
    # Memory Access
    memory_fetch = self.memory.Data_Operate(alu_result, read_data_2, self.controller.MemRead, self.controller.MemWrite, self.controller.ALUOp)  
    
    # Write Back
    self.write_back = HW.Write_Back_Mux(memory_fetch, alu_result, self.controller.MemToReg)

    # Write back to Register File
    self.Register_File.Operate(self.decoder.rs, self.decoder.rt, write_reg, self.write_back, (self.controller.RegWrite | alu_reg_set) )


  def run(self):
    sp = REG_DICT["sp"]
    fp = REG_DICT["fp"]

    self.Register_File.Set(sp, self.memory.Load_Word(0))
    self.Register_File.Set(fp, self.memory.Load_Word(4))
    self.PC.Set(self.memory.Load_Word(20))
    while(not self.PROGRAM_EXIT):
      self.cycle()


if __name__ == "__main__":
  with open("example.txt", "r") as f:
    contents = f.readlines()
  
  contents = [int(line.split(",")[0].strip(), 16) for line in contents]
  sim = Single_Cycle(contents)
  sim.run()
  
