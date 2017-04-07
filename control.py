from enum import IntEnum, unique
#from opcode import FUNCT, OP
import opcode

@unique
class ALUEnum(IntEnum):
    X     = 0
    AND   = 1
    OR    = 2
    ADD   = 3
    ADDU  = 4
    SUB   = 5
    SUBU  = 6
    SLL   = 7
    SRL   = 8
    SLT   = 9
    NOT   = 10
    LOAD  = 11
    STORE = 12

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

  __funct_dic = {
    opcode.FUNCT.SLL  : ALUEnum.SLL,
    opcode.FUNCT.SRL  : ALUEnum.SRL,
    opcode.FUNCT.JR   : ALUEnum.X,
    opcode.FUNCT.ADD  : ALUEnum.ADD,
    opcode.FUNCT.ADDU : ALUEnum.ADDU,
    opcode.FUNCT.SUB  : ALUEnum.SUB,
    opcode.FUNCT.SUBU : ALUEnum.SUBU,
    opcode.FUNCT.AND  : ALUEnum.AND,
    opcode.FUNCT.OR   : ALUEnum.OR,
    opcode.FUNCT.NOR  : ALUEnum.NOR,
    opcode.FUNCT.SLT  : ALUEnum.SLT,
    opcode.FUNCT.SLLU : ALUEnum.SLTU
  }

  def update(self, op, funct):
    # TODO: Assert on bounds
    if op == OP.RTYPE:
      self.RegDst   = 1
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = self.__funct_dic[FUNCT(funct)]

    elif op == OP.J:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 1
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.X

    elif op == OP.JAL:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 1
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.X
      # TODO: Need a way to set a register

    elif op == OP.BEQ:
      self.RegDst   = 0
      self.Branch   = 1
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.BEQ

    elif op == OP.BNE:
      self.RegDst   = 0
      self.Branch   = 1
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.BNE

    elif op == OP.ADDI:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.ADD

    elif op == OP.ADDIU:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.ADDU

    elif op == OP.SLTI:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.SLT

    elif op == OP.SLTIU:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.SLTU

    elif op == OP.ANDI:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.AND

    elif op == OP.ORI:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 0
      self.ALUSrc   = 0
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.OR

    elif op == OP.LUI:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.LOAD

    elif op == OP.LW:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.LOAD

    elif op == OP.LBU:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.LOAD

    elif op == OP.LHU:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 1
      self.MemToReg = 1
      self.MemWrite = 0
      self.ALUSrc   = 1
      self.RegWrite = 1
      self.ALUOp    = ALUEnum.LOAD

    elif op == OP.SB:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.STORE

    elif op == OP.SH:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.STORE

    elif op == OP.SW:
      self.RegDst   = 0
      self.Branch   = 0
      self.Jump     = 0
      self.MemRead  = 0
      self.MemToReg = 0
      self.MemWrite = 1
      self.ALUSrc   = 1
      self.RegWrite = 0
      self.ALUOp    = ALUEnum.STORE
    else:
      assert 0 == 1, "Operation not supported: %s" % op
