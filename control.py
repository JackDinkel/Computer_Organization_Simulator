
ALU_DICT = {
  "X"     : 0,
  "AND"   : 1,
  "OR"    : 2,
  "ADD"   : 3,
  "ADDU"  : 4,
  "SUB"   : 5,
  "SUBU"  : 6,
  "SLL"   : 7,
  "SRL"   : 8,
  "SLT"   : 9,
  "SLTU"  : 10,
  "NOT"   : 11,
  "LW"    : 12,
  "LH"    : 13,
  "LB"    : 14,
  "LHU"   : 15,
  "LBU"   : 16,
  "SW"    : 17,
  "SH"    : 18,
  "SB"    : 19,
  "NOR"   : 20,
  "MOVZ"  : 21,
  "MOVN"  : 22,
  "XOR"   : 23,
}

class Controller(object):
  RegDst   = 0 # Control to Register_Input_MUX, 0 if I-type, 1 if R-type
  Branch   = 0 # First control to PC_Input_MUX, 0 to use incremented PC, 1 to use Branch address
  Jump     = 0 # Second control to PC_Input_MUX, 0 to use value from above, 1 to use Jump address
  MemRead  = 0 # Set to 1 to fetch from Memory
  MemWrite = 0 # Set to 1 to read from Memory
  MemToReg = 0 # Control to Write_Back_MUX, 0 to use ALU result, 1 to use Memory
  ALUOp    = 0 # Control to ALU, which operation to perform
  ALUSrc   = 0 # Control to ALU_Input_MUX, 0 to use Register, 1 to use immediate
  RegWrite = 0 # Set to 1 to write a new value to a register

  __funct_dic = {
    0x00 : ALU_DICT["SLL"],  # SLL
    0x02 : ALU_DICT["SRL"],  # SRL
    0x08 : ALU_DICT["X"],    # JR
    0x0A : ALU_DICT["MOVZ"], # MOVZ
    0x0B : ALU_DICT["MOVN"], # MOVN
    0x20 : ALU_DICT["ADD"],  # ADD
    0x21 : ALU_DICT["ADDU"], # ADDU
    0x22 : ALU_DICT["SUB"],  # SUB
    0x23 : ALU_DICT["SUBU"], # SUBU
    0x24 : ALU_DICT["AND"],  # AND
    0x25 : ALU_DICT["OR"],   # OR
    0x27 : ALU_DICT["NOR"],  # NOR
    0x26 : ALU_DICT["XOR"],  # XOR
    0x2A : ALU_DICT["SLT"],  # SLT
    0x2B : ALU_DICT["SLTU"]  # SLTU
  }

  def display(self):
    print "RegDst:", self.RegDst
    print "Branch:", self.Branch
    print "Jump:", self.Jump
    print "MemRead:", self.MemRead
    print "MemWrite:", self.MemWrite
    print "MemToReg:", self.MemToReg
    print "ALUOp:", self.ALUOp
    print "ALUSrc:", self.ALUSrc
    print "RegWrite:", self.RegWrite

  def update(self, op, funct):
    # TODO: Assert on bounds
    if op == 0x00: # RTYPE
      self.RegDst   = 1
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = self.__funct_dic[funct]

    elif op == 0x01: # BLTZ TODO
      pass

    elif op == 0x02: # J
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 1
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["X"]

    elif op == 0x03: # JAL
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 1
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["X"]
      # TODO: Need a way to set a register

    elif op == 0x04: # BEQ
      self.RegDst   = 0
      self.Branch   = 1
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["BEQ"]

    elif op == 0x05: # BNE
      self.RegDst   = 0
      self.Branch   = 1
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["BNE"]

    elif op == 0x06: # BLTZ TODO
      pass

    elif op == 0x07: # BGTZ TODO
      pass

    elif op == 0x08: # ADDI
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["ADD"]

    elif op == 0x09: # ADDIU
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["ADDU"]

    elif op == 0x0A: # SLTI
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["SLT"]

    elif op == 0x0B: # SLTIU
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["SLTU"]

    elif op == 0x0C: # ANDI
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["AND"]

    elif op == 0x0D: # ORI
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["OR"]

    elif op == 0x0E: # XORI TODO
      pass

    elif op == 0x0F: # LUI TODO
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["LOAD"]

    elif op == 0x1F: # SEP TODO
      pass

    elif op == 0x20: # LB TODO
      pass

    elif op == 0x21: # LH TODO
      pass

    elif op == 0x23: # LW
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["LW"]

    elif op == 0x24: # LBU
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["LBU"]

    elif op == 0x25: # LHU
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALU_DICT["LHU"]

    elif op == 0x28: # SB
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["SB"]

    elif op == 0x29: # SH
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["SH"]

    elif op == 0x2B: # SW
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALU_DICT["SW"]

    else:
      assert 0 == 1, "Operation not supported: %s" % op

