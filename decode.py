import mask

class Instruction:
  word  = 0
  op    = 0
  rs    = 0
  rt    = 0
  rd    = 0
  shamt = 0 
  funct = 0
  i_imm = 0
  j_imm = 0

def displayInstruction(instr):
  print "op:", instr.op
  print "rs:", instr.rs
  print "rt:", instr.rt
  print "rd:", instr.rd
  print "shamt:", instr.shamt
  print "funct:", instr.funct
  print "i_imm:", instr.i_imm
  print "j_imm:", instr.j_imm

def decodeInstruction(instr):
  value = instr.word
  instr.op    = mask.Get_Bits_31_26(value)
  instr.rs    = mask.Get_Bits_25_21(value)
  instr.rt    = mask.Get_Bits_20_16(value)
  instr.rd    = mask.Get_Bits_15_11(value)
  instr.shamt = mask.Get_Bits_10_6(value)
  instr.funct = mask.Get_Bits_5_0(value)
  instr.i_imm = mask.Get_Bits_15_0(value)
  instr.j_imm = mask.Get_Bits_25_0(value)
  if instr.op == 0x03: # JAL, set rd to reg31
    instr.rd = 31
