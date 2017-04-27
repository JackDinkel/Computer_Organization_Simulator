import mask

class Decoder:
  instruction = 0
  op    = 0
  rs    = 0
  rt    = 0
  rd    = 0
  shamt = 0 
  funct = 0
  i_imm = 0
  j_imm = 0

  def display(self):
    print "instr:", hex(self.instruction)
    print "op:", self.op
    print "rs:", self.rs
    print "rt:", self.rt
    print "rd:", self.rd
    print "shamt:", self.shamt
    print "funct:", self.funct
    print "i_imm:", hex(self.i_imm)
    print "j_imm:", hex(self.j_imm)

  def decode(self, instr):
    self.instruction = instr
    self.op    = mask.Get_Bits_31_26(instr)
    self.rs    = mask.Get_Bits_25_21(instr)
    self.rt    = mask.Get_Bits_20_16(instr)
    self.rd    = mask.Get_Bits_15_11(instr)
    self.shamt = mask.Get_Bits_10_6(instr) # TODO: Do we need this?
    self.funct = mask.Get_Bits_5_0(instr)
    self.i_imm = mask.Get_Bits_15_0(instr)
    self.j_imm = mask.Get_Bits_25_0(instr) # TODO

    if self.op == 0x03: # JAL, set rd to reg31
      self.rd = 31
