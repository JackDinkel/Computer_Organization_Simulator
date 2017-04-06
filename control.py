class Controller:
  RegDst   = 0 # Control to Register_Input_MUX, 0 if I-type, 1 if R-type
  Branch   = 0 # First control to PC_Input_MUX, 0 to use incremented PC, 1 to use Branch address
  Jump     = 0 # Second control to PC_Input_MUX, 0 to use value from above, 1 to use Jump address
  MemRead  = 0 # Set to 1 to fetch from Memory
  MemWrite = 0 # Set to 1 to read from Memory
  MemToReg = 0 # Control to Write_Back_MUX, 0 to use ALU result, 1 to use Memory
  ALUOp    = 0 # ???
  ALUSrc   = 0 # Control to ALU_Input_MUX, 0 to use Register, 1 to use immediate
  RegWrite = 0 # Set to 1 to write a new value to a register

  def update(self, op):
    if op == 0x00: # R-type
      self.RegDst   = 1
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x02: # j
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 1
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0

    elif op == 0x03: # jal
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 1
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0

    elif op == 0x04: # beq
      self.RegDst   = 0
      self.Branch   = 1
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0

    elif op == 0x05: # bne
      self.RegDst   = 0
      self.Branch   = 1
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0

    elif op == 0x08: # addi
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x09: # addiu
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x0A: # slti
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x0B: # sltiu
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x0C: # andi
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x0D: # ori
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1

    elif op == 0x0F: # lui
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1

    elif op == 0x23: # lw
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1

    elif op == 0x24: # lbu
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1

    elif op == 0x25: # lhu
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      #self.ALUOp    = 
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1

    elif op == 0x28: # sb
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0

    elif op == 0x29: # sh
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0

    elif op == 0x2B: # sw
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      #self.ALUOp    = 
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
    else:
      assert 0 == 1, "Operation not supported: %s" % op
