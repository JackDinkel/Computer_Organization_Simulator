OP_DICT = {
  "NOP"   : 0x00, # tested
  "ADD"   : 0x00, # tested
  "ADDU"  : 0x00,
  "AND"   : 0x00, # tested
  "JR"    : 0x00, # tested
  "NOR"   : 0x00, # tested
  "OR"    : 0x00, # tested
  "MOVN"  : 0x00, # tested
  "MOVZ"  : 0x00, # tested
  "SLT"   : 0x00, # tested
  "SLTU"  : 0x00,
  "SLL"   : 0x00, # tested
  "SRL"   : 0x00, # tested
  "SUB"   : 0x00, # tested
  "SUBU"  : 0x00,
  "XOR"   : 0x00, # tested
  "ADDI"  : 0x08, # tested
  "ADDIU" : 0x09,
  "ANDI"  : 0x0C, # tested
  "XORI"  : 0x0E, # tested
  "BEQ"   : 0x04, # tested
  "BNE"   : 0x05, # tested
  "BGTZ"  : 0x07, # tested
  "BLTZ"  : 0x01, # tested
  "BLEZ"  : 0x06, # tested
  "J"     : 0x02, # tested
  "JAL"   : 0x03, # tested
  "LB"    : 0x20,
  "LBU"   : 0x24,
  "LH"    : 0x21,
  "LHU"   : 0x25,
  "LUI"   : 0x0F,
  "LW"    : 0x23, # tested
  "ORI"   : 0x0D, # tested
  "SLTI"  : 0x0A, # tested
  "SLTIU" : 0x0B,
  "SB"    : 0x28,
  "SH"    : 0x29,
  "SW"    : 0x2B, # tested
  "SEB"   : 0x1F
}


FUNCT_DICT = {
  "NOP"   : 0x00,
  "ADD"   : 0x20,
  "ADDU"  : 0x21,
  "AND"   : 0x24,
  "JR"    : 0x08,
  "NOR"   : 0x27,
  "OR"    : 0x25,
  "MOVN"  : 0x0B,
  "MOVZ"  : 0x0A,
  "SLT"   : 0x2A,
  "SLTU"  : 0x2B,
  "SLL"   : 0x00,
  "SRL"   : 0x02,
  "SUB"   : 0x22,
  "SUBU"  : 0x23,
  "XOR"   : 0x26
  #"ADDI"  : 
  #"ADDIU" : 
  #"ANDI"  : 
  #"XORI"  : 
  #"BEQ"   : 
  #"BNE"   : 
  #"BGTZ"  :   
  #"BLTZ"  :   
  #"BLEZ"  :   
  #"J"     : 
  #"JAL"   : 
  #"LB"    : 
  #"LBU"   : 
  #"LH"    : 
  #"LHU"   : 
  #"LUI"   :   
  #"LW"    : 
  #"ORI"   : 
  #"SLTI"  : 
  #"SLTIU" : 
  #"SB"    : 
  #"SH"    : 
  #"SW"    : 
  #"SEB"   :
}
