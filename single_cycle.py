import hardware as HW
import decode
import control

# Address of the first instruction
first_instr = 0x0


# Initialize helpers
decoder    = decode.Decoder()
controller = control.Controller()


# Initialize hardware
PC = HW.PC()
Instruction_Memory = HW.Instruction_Memory()
Register_File = HW.Register_File()
Data_Memory = HW.Data_Memory()


# Fill Instruction Memory
Instruction_Memory.Add_Word(0x00000000)


# Initialize local variables
write_back = 0
next_pc = first_instr
incremented_pc = 0
branch_addr = 0
jump_addr = 0


### Execute ###

# Instruction Fetch
next_pc = HW.PC_Input_Mux(incremented_pc, branch_addr, jump_addr, controller.Branch, controller.Jump)
PC.Update(next_pc)
current_pc = PC.Get()
current_instr = Instruction_Memory.Fetch_Word(current_pc)
incremented_pc = HW.Add_Four(current_pc)

# Instruction Decode and Register File Read
decoder.decode(current_instr)
controller.update(decoder.op)
read_data_1, read_data_2 = Register_File.Operate(decoder.op, decoder.rs, decoder.rt, write_back, controller.RegWrite)

# Execute and Adress Calculation
extended_i_imm = HW.Sign_Extend(decoder.i_imm)
alu_operand_2 = HW.ALU_Input_Mux(read_data_2, extended_i_imm, controller.ALUSrc)
ALU_Control = 0 # TODO
alu_result, zero = HW.ALU(read_data_1, alu_operand_2, ALU_Control)
shifted_i_imm = HW.Shift_Left_2(extended_i_imm)
branch_addr = HW.Address_Adder(incremented_pc, shifted_i_imm)
jump_addr = HW.Calculate_Jump_Addr(decoder.j_imm, incremented_pc)

# Memory Access
memory_fetch = Data_Memory.Operate(alu_result, read_data_2, controller.MemRead, controller.MemWrite)  

# Write Back
write_back = HW.Write_Back_Mux(memory_fetch, alu_result, controller.MemToReg)
