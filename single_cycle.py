import hardware as HW
import decode
from control import Controller

class Single_Cycle(object):
  # Address of the first instruction
  first_instr = 0x0
  mem_size = 1200
  
  
  # Initialize helpers
  decoder    = decode.Decoder()
  controller = Controller()
  
  
  # Initialize hardware
  PC = HW.PC()
  memory = HW.Memory(mem_size)
  Register_File = HW.Register_File()


  # Initialize variables
  write_back = 0
  next_pc = first_instr
  incremented_pc = 0
  branch_addr = 0
  jump_addr = 0


  def cycle(self):
   
    ### Execute ###
    # Instruction Fetch
    self.next_pc = HW.PC_Input_Mux(self.incremented_pc, self.branch_addr, self.jump_addr, self.controller.Branch, self.controller.Jump)
    self.PC.Update(self.next_pc)
    current_pc = self.PC.Get()
    current_instr = self.memory.Instruction_Operate(current_pc, 0, 1, 0)  
    self.incremented_pc = HW.Add_Four(current_pc)
    
    # Instruction Decode and Register File Read
    self.decoder.decode(current_instr)
    self.controller.update(self.decoder.op, self.decoder.funct)
    write_reg = HW.Register_Input_Mux(self.decoder.rt, self.decoder.rd, self.controller.RegDst) 

    # Register Read
    read_data_1, read_data_2 = self.Register_File.Operate(self.decoder.rs, self.decoder.rt, write_reg, self.write_back, 0)
    
    # Execute and Adress Calculation
    extended_i_imm = HW.Sign_Extend(self.decoder.i_imm, 16)
    alu_operand_2 = HW.ALU_Input_Mux(read_data_2, extended_i_imm, self.controller.ALUSrc)
    alu_result, zero = HW.ALU(read_data_1, alu_operand_2, self.decoder.shamt, self.controller.ALUOp)
    alu_result = HW.twos_comp(alu_result, 32)
    shifted_i_imm = HW.Shift_Left_2(extended_i_imm)
    self.branch_addr = HW.Address_Adder(self.incremented_pc, shifted_i_imm)
    self.jump_addr = HW.Calculate_Jump_Addr(self.decoder.j_imm, self.incremented_pc)
    
    # Memory Access
    memory_fetch = self.memory.Data_Operate(alu_result, read_data_2, self.controller.MemRead, self.controller.MemWrite)  
    
    # Write Back
    self.write_back = HW.Write_Back_Mux(memory_fetch, alu_result, self.controller.MemToReg)

    # Write back to Register File
    self.Register_File.Operate(self.decoder.rs, self.decoder.rt, write_reg, self.write_back, self.controller.RegWrite)


if __name__ == "__main__":
  simulator = Single_Cycle()

  # Fill Instruction Memory
  simulator.memory.Add_Word(0x00000000)
  
  simulator.execute()
  
  
