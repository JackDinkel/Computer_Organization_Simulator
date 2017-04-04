import mask

class Decoder:
  op    = 0
  rs    = 0
  rt    = 0
  rd    = 0
  shamt = 0 
  funct = 0
  i_imm = 0
  j_imm = 0

  def decode(self, instr):
    self.op    = mask.Get_Bits_31_26(instr)
    self.rs    = mask.Get_Bits_25_21(instr)
    self.rt    = mask.Get_Bits_20_16(instr)
    self.rd    = mask.Get_Bits_15_11(instr)
    self.shamt = mask.Get_Bits_10_6(instr) # TODO: Do we need this?
    self.funct = mask.Get_Bits_5_0(instr)
    self.i_imm = mask.Get_Bits_15_0(instr)
    self.j_imm = mask.Get_Bits_25_0(instr) # TODO
