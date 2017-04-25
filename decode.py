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

def displayInstruction(self, instr):
  print "op:", self.op
  print "rs:", self.rs
  print "rt:", self.rt
  print "rd:", self.rd
  print "shamt:", self.shamt
  print "funct:", self.funct
  print "i_imm:", self.i_imm
  print "j_imm:", self.j_imm

def decodeInstruction(self, instr):
  value = instr.word
  instr.op    = mask.Get_Bits_31_26(value)
  instr.rs    = mask.Get_Bits_25_21(value)
  instr.rt    = mask.Get_Bits_20_16(value)
  instr.rd    = mask.Get_Bits_15_11(value)
  instr.shamt = mask.Get_Bits_10_6(value) # TODO: Do we need this?
  instr.funct = mask.Get_Bits_5_0(value)
  instr.i_imm = mask.Get_Bits_15_0(value)
  instr.j_imm = mask.Get_Bits_25_0(value) # TODO
