from control import ALU_DICT
from util import *

def ALU(input1, input2, shamt, ALUControl):
  print "AluControl:", ALUControl
  print "ALU+DICT[j]", ALU_DICT["J"]
  if   ALUControl == ALU_DICT["J"]:
    return 0, 1, 0
  elif ALUControl == ALU_DICT["AND"]:
    return input1 & input2, 0, 0
  elif ALUControl == ALU_DICT["OR"]:
    return input1 | input2, 0, 0
  elif ALUControl == ALU_DICT["ADD"]:
    input1 = twos_comp(input1, 32)
    input2 = twos_comp(input2, 32)
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["ADDU"]:
    return unsigned(input1, 32) + unsigned(input2, 32), 0, 0 # TODO
  elif ALUControl == ALU_DICT["SUB"]:
    input1 = twos_comp(input1, 32)
    input2 = twos_comp(input2, 32)
    return input1 - input2, 0, 0
  elif ALUControl == ALU_DICT["SUBU"]:
    return unsigned(input1, 32) - unsigned(input2, 32), 0, 0 # TODO
  elif ALUControl == ALU_DICT["SLL"]:
    return input2 << shamt, 0, 0
  elif ALUControl == ALU_DICT["SRL"]:
    return logical_rshift(input2, shamt), 0, 0
  elif ALUControl == ALU_DICT["SLT"]:
    return ( input1 < input2 ), 0, 1 # TODO
  elif ALUControl == ALU_DICT["SLTU"]:
    return ( unsigned(input1, 32) < unsigned(input2, 32) ), 0, 1 # TODO
  elif ALUControl == ALU_DICT["NOT"]:
    return ~input1, 0, 0
  elif ALUControl == ALU_DICT["LW"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LH"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LB"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LHU"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LBU"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["LUI"]:
    return (input2 << 16) | (input1 & 0x0000FFFF), 0, 0
  elif ALUControl == ALU_DICT["SW"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["SH"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["SB"]:
    return input1 + input2, 0, 0
  elif ALUControl == ALU_DICT["NOR"]:
    return ~(input1 | input2), 0, 0
  elif ALUControl == ALU_DICT["MOVZ"]:
    return (input1, 0, 1) if input2 == 0 else (0, 0, 0) # TODO
  elif ALUControl == ALU_DICT["MOVN"]:
    return (input1, 0, 1) if input2 != 0 else (0, 0, 0) # TODO
  elif ALUControl == ALU_DICT["XOR"]:
    return (input1 ^ input2), 0, 0
  elif ALUControl == ALU_DICT["BLTZ"]:
    return (0, 1, 0) if input1 < 0 else (0, 0, 0)
  elif ALUControl == ALU_DICT["BLEZ"]:
    return (0, 1, 0) if input1 <= 0 else (0, 0, 0)
  elif ALUControl == ALU_DICT["BGTZ"]:
    return (0, 1, 0) if input1 > 0 else (0, 0, 0)
  elif ALUControl == ALU_DICT["J"]:
    return 0, 0, 0
  elif ALUControl == ALU_DICT["JAL"]:
    return "pc", 0, 1 # TODO
  elif ALUControl == ALU_DICT["BEQ"]:
    return (0, 0, 1) if input1 == input2 else (0, 0, 0)
  elif ALUControl == ALU_DICT["BNE"]:
    return (0, 0, 1) if input1 != input2 else (0, 0, 0)
  else:
    assert 1 == 2, "Invalid Operation: %s" % ALUControl
