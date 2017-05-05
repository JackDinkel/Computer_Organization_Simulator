from util import *

def MUX(input1, input2, control):
  assert control == 0 or control == 1, "control out of bounds: %s" % control

  if control == 0:
    return input1
  else:
    return input2


def PC_Input_Mux(incremented, branch_addr, jump_addr, Branch, Jump):
  # TODO: This needs a closer look, page 271
  mux1 = MUX(incremented, branch_addr, Branch)
  return MUX(mux1, jump_addr, Jump)


def Register_Input_Mux(i_type_reg, r_type_reg, RegDst):
  return MUX(i_type_reg, r_type_reg, RegDst)


def ALU_Input_Mux1(register1, register2, ALUSrc1):
  return MUX(register1, register2, ALUSrc1)


def ALU_Input_Mux2(register, sign_extended, ALUSrc2):
  return MUX(register, sign_extended, ALUSrc2)


def Hazard_Detection_Mux(exc, memc, wbc, hazard):
  if hazard == 1:
    exc.RegDst    = 0
    memc.Branch   = 0
    memc.Jump     = 0
    memc.MemRead  = 0
    wbc.MemToReg  = 0
    memc.MemWrite = 0
    exc.ALUSrc    = 0
    wbc.RegWrite  = 0
    exc.ALUOp     = 0
  return exc, memc, wbc


def ALU_Reg_A_Mux(reg_data_1, write_back, alu_result, forwardA):
  assert forwardA >= 0 and forwardA <= 2, "forwardA out of bounds: %d" % forwardA
  if forwardA == 0:
    return reg_data_1
  elif forwardA == 1:
    return write_back
  elif forwardA == 2:
    return alu_result
  else:
    return 0


def ALU_Reg_B_MUX(reg_data_2, write_back, alu_result, forwardB):
  assert forwardB >= 0 and forwardB <= 2, "forwardB out of bounds: %d" % forwardB
  if forwardB == 0:
    return reg_data_2
  elif forwardB == 1:
    return write_back
  elif forwardB == 2:
    return alu_result
  else:
    return 0


def Write_Back_Mux(Read_Data, ALU_Result, MemToReg):
  return MUX(ALU_Result, Read_Data, MemToReg)
