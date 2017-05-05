'''
  Conventions and design:
    All hardware constructs are First_Letter_Capitalized_And_Word_Separated_By_Underscore
    All local variables are lower_case_and_word_separated_by_underscore
    All hardware control logic lines are CapitalCamelCase

    Each component of the computer diagrams in the book has a corresponding function or class
    Components that have state are classes
    Components that are combinatorial are functions with inputs and outputs

    The general idea is to emulate hardware, so each function is always called whether or not
    it is actually needed, and multiplexors make the decisions
'''

from control import ALU_DICT
from opcode import *
from util import *
import mask


def Add_Four(input_num):
  #TODO: Error bounds
  return input_num + 4 # Only add 1 for Word Address


def Hazard_Detection_Unit(memread, idex_rt, ifid_rs, ifid_rt):
  if ((memread == 1) and ((idex_rt == ifid_rt) or (idex_rt == ifid_rs))):
    return 1
  else:
    return 0
def Shift_Left_2(unshifted_num):
  return unshifted_num << 2 # Using Word Addresses


def Calculate_Jump_Addr(unshifted_num, rs_val, next_pc, jr):
  # This takes the place of the shift left 2 and concatenation components on page 271
  # TODO: assert unshifted_num is in bounds (26 bits)
  if jr:
    return rs_val
  else:
    mask = 0xF0000000
    pc_upper = next_pc & mask
    return (unshifted_num << 2) + pc_upper # Using Word Addresses


def Address_Adder(next_pc, shifted_num):
  return next_pc + shifted_num


def Hazard_Detection_Unit(memread, idex_rt, ifid_rs, ifid_rt):
  if ((memread == 1) and ((idex_rt == ifid_rt) or (idex_rt == ifid_rs))):
    return 1
  else:
    return 0


def Sign_Extend_Immediate(input_val):
  if input_val >= 0x8000:
    return -( (input_val ^ 0xffff) + 1)
  else:
    return input_val


# see figures 4.56 and 4.57
def Forwarding_Unit(idex_rs, idex_rt, exmem_rd, memwb_rd, exmem_reg_write, memwb_reg_write):
  forwardA = 0
  forwardB = 0

  if (exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rs):
    forwardA = 2

  if (exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rt):
    forwardB = 2

  if ((memwb_reg_write == 1) and (memwb_rd != 0) and 
    not ((exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rs)) 
    and (memwb_rd == idex_rs)):
    forwardA = 1

  if ((memwb_reg_write == 1) and (memwb_rd != 0) and 
    not ((exmem_reg_write == 1) and (exmem_rd != 0) and (exmem_rd == idex_rt)) 
    and (memwb_rd == idex_rt)):
    forwardB = 1

  return forwardA, forwardB


