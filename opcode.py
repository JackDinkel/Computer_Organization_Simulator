
OP_DICT = {
  #"NOP"   :     
  #"SLL"   : 0x00
  #"SRL"   : 0x00
  #"JR"    : 0x00
  #"ADD"   : 0x00
  #"ADDU"  : 0x00
  #"SUB"   : 0x00
  #"SUBU"  : 0x00
  #"AND"   : 0x00
  #"OR"    : 0x00
  #"NOR"   : 0x00
  #"SLT"   : 0x00
  #"SLTU"  : 0x00
  #"MOVN"  :     
  #"MOVZ"  :     
  #"XOR"   :     
  "RTYPE" : 0x00,
  "J"     : 0x02,
  "JAL"   : 0x03,
  "BEQ"   : 0x04,
  "BNE"   : 0x05,
  "ADDI"  : 0x08, #tested
  "ADDIU" : 0x09,
  "SLTI"  : 0x0A, #tested
  "SLTIU" : 0x0B,
  "ANDI"  : 0x0C,
  "ORI"   : 0x0D,
  "LUI"   : 0x0F,
  "LW"    : 0x23, #tested
  "LBU"   : 0x24,
  "LHU"   : 0x25,
  "SB"    : 0x28,
  "SH"    : 0x29,
  "SW"    : 0x2B #tested
  #"XORI"  =     
  #"BGTZ"  =     
  #"BLTZ"  =     
  #"BLEZ"  =     
}

FUNCT_DICT = {
  #NOP   =     
  "SLL"   : 0x00, #tested
  "SRL"   : 0x02,
  "JR"    : 0x08,
  "ADD"   : 0x20, #tested
  "ADDU"  : 0x21,
  "SUB"   : 0x22, #tested
  "SUBU"  : 0x23,
  "AND"   : 0x24,
  "OR"    : 0x25,
  "NOR"   : 0x27,
  "SLT"   : 0x2A,
  "SLTU"  : 0x2B
  #MOVN  =     
  #MOVZ  =     
  #XOR   =     
  #J     = 0x00
  #JAL   = 0x00
  #BEQ   = 0x00
  #BNE   = 0x00
  #ADDI  = 0x00
  #ADDIU = 0x00
  #SLTI  = 0x00
  #SLTIU = 0x00
  #ANDI  = 0x00
  #ORI   = 0x00
  #LUI   = 0x00
  #LW    = 0x00
  #LBU   = 0x00
  #LHU   = 0x00
  #SB    = 0x00
  #SH    = 0x00
  #SW    = 0x00
  ##XORI  =     
  #BGTZ  =     
  #BLTZ  =     
  #BLEZ  =     
}

