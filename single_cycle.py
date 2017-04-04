import hardware as HW
import decode

# Address of the first instruction
first_instr = 0x0


# Initialize helpers
decoder = decode.Decoder()

# Initialize hardware
PC = HW.PC(first_instr)
Instruction_Memory = HW.Instruction_Memory()

# Fill Instruction Memory
Instruction_Memory.Add_New_Instruction(0x00000000)

# Execute
current_pc = PC.Get()
current_instr = Instruction_Memory.Fetch_Instruction(current_pc)
decoder.decode(current_instr)



