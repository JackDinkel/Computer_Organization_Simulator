
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
  "LUI"   : 24,
  "BLTZ"  : 25,
  "BLEZ"  : 26,
  "BGTZ"  : 27,
  "J"     : 28,
  "JAL"   : 29,
  "BEQ"   : 30,
  "BNE"   : 31,
}

class EXControl(object):
  RegDst   = 0 # Control to Register_Input_MUX, 0 if I-type, 1 if R-type
  ALUOp    = 0 # Control to ALU, which operation to perform
  ALUSrc   = 0 # Control to ALU_Input_MUX, 0 to use Register, 1 to use immediate

class MEMControl(object):
  Branch   = 0 # First control to PC_Input_MUX, 0 to use incremented PC, 1 to use Branch address
  MemRead  = 0 # Set to 1 to fetch from Memory
  MemWrite = 0 # Set to 1 to read from Memory
  Jump     = 0 # Second control to PC_Input_MUX, 0 to use value from above, 1 to use Jump address

class WBControl(object):
  RegWrite = 0 # Set to 1 to write a new value to a register
  MemToReg = 0 # Control to Write_Back_MUX, 0 to use ALU result, 1 to use Memory

funct_dic = {
  0x00 : ALU_DICT["SLL"],  # SLL
  0x02 : ALU_DICT["SRL"],  # SRL
  0x08 : ALU_DICT["J"],    # JR
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

def displayControl(exc, memc, wbc):
  print "RegDst:", exc.RegDst
  print "Branch:", memc.Branch
  print "Jump:", memc.Jump
  print "MemRead:", memc.MemRead
  print "MemWrite:", memc.MemWrite
  print "MemToReg:", wbc.MemToReg
  print "ALUOp:", exc.ALUOp
  print "ALUSrc:", exc.ALUSrc
  print "RegWrite:", wbc.RegWrite

def updateControl(op, funct, exc, memc, wbc):
  # TODO: Assert on bounds
  if op == 0x00: # RTYPE
    exc.RegDst    = 1
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 0
    wbc.RegWrite  = 1
    exc.ALUOp     = funct_dic[funct]

  elif op == 0x01: # BLTZ
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 1
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["BLTZ"]

  elif op == 0x02: # J
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 1
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["X"]

  elif op == 0x03: # JAL
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 1
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["X"]

  elif op == 0x04: # BEQ
    exc.RegDst    = 0
    memc.Branch   = 1
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["X"]

  elif op == 0x05: # BNE
    exc.RegDst    = 0
    memc.Branch   = 1
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["X"]

  elif op == 0x06: # BLEZ
    exc.RegDst    = 0
    memc.Branch   = 1
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["BLEZ"]
    pass

  elif op == 0x07: # BGTZ
    exc.RegDst    = 0
    memc.Branch   = 1
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["BGTZ"]
    pass

  elif op == 0x08: # ADDI
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["ADD"]

  elif op == 0x09: # ADDIU
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["ADDU"]

  elif op == 0x0A: # SLTI
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["SLT"]

  elif op == 0x0B: # SLTIU
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["SLTU"]

  elif op == 0x0C: # ANDI
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["AND"]

  elif op == 0x0D: # ORI
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["OR"]

  elif op == 0x0E: # XORI
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["XOR"]

  elif op == 0x0F: # LUI
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["LUI"] # TODO: whyyy was AluSrc1 = 1 ???

  elif op == 0x1F: # SEP TODO
    pass

  elif op == 0x20: # LB
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 1
    wbc.MemToReg  = 1
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["LB"]

  elif op == 0x21: # LH
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 1
    wbc.MemToReg  = 1
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["LH"]

  elif op == 0x23: # LW
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 1
    wbc.MemToReg  = 1
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["LW"]

  elif op == 0x24: # LBU
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 1
    wbc.MemToReg  = 1
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["LBU"]

  elif op == 0x25: # LHU
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 1
    wbc.MemToReg  = 1
    memc.MemWrite = 0
    exc.ALUSrc    = 1
    wbc.RegWrite  = 1
    exc.ALUOp     = ALU_DICT["LHU"]

  elif op == 0x28: # SB
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 1
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["SB"]

  elif op == 0x29: # SH
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 1
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["SH"]

  elif op == 0x2B: # SW
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 1
    exc.ALUSrc    = 1
    wbc.RegWrite  = 0
    exc.ALUOp     = ALU_DICT["SW"]

  else:
    assert 0 == 1, "Operation not supported: %s" % op

