OP_DICT = {
  "NOP"   : 0x00,
  "ADD"   : 0x00,
  "ADDU"  : 0x00,
  "AND"   : 0x00,
  "JR"    : 0x00,
  "NOR"   : 0x00,
  "OR"    : 0x00,
  "MOVN"  : 0x00,
  "MOVZ"  : 0x00,
  "SLT"   : 0x00,
  "SLTU"  : 0x00,
  "SLL"   : 0x00,
  "SRL"   : 0x00,
  "SUB"   : 0x00,
  "SUBU"  : 0x00,
  "XOR"   : 0x00,
  "ADDI"  : 0x08,
  "ADDIU" : 0x09,
  "ANDI"  : 0x0C,
  "XORI"  : 0x0E,
  "BEQ"   : 0x04,
  "BNE"   : 0x05,
  "BGTZ"  : 0x07,
  "BLTZ"  : 0x01,
  "BLEZ"  : 0x06,
  "J"     : 0x02,
  "JAL"   : 0x03,
  "LB"    : 0x20,
  "LBU"   : 0x24,
  "LH"    : 0x21,
  "LHU"   : 0x25,
  "LUI"   : 0x0F,
  "LW"    : 0x23,
  "ORI"   : 0x0D,
  "SLTI"  : 0x0A,
  "SLTIU" : 0x0B,
  "SB"    : 0x28,
  "SH"    : 0x29,
  "SW"    : 0x2B,
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
