from add_sp_plus_immediate_t2 import AddSpPlusImmediateT2
from sub_sp_minus_immediate_t1 import SubSpMinusImmediateT1
from cbz_t1 import CbzT1
from sxth_t1 import SxthT1
from sxtb_t1 import SxtbT1
from uxth_t1 import UxthT1
from uxtb_t1 import UxtbT1
from push_t1 import PushT1
from setend_t1 import SetendT1
from cps_thumb_t1 import CpsThumbT1
from rev_t1 import RevT1
from rev16_t1 import Rev16T1
from revsh_t1 import RevshT1
from pop_thumb_t1 import PopThumbT1
from bkpt_t1 import BkptT1
import thumb_if_then_and_hints


def decode_instruction(instr):
    if instr[4:9] == "0b00000":
        # Add Immediate to SP
        return AddSpPlusImmediateT2
    elif instr[4:9] == "0b00001":
        # Subtract Immediate from SP
        return SubSpMinusImmediateT1
    elif instr[4:8] == "0b0001":
        # Compare and Branch on Zero
        return CbzT1
    elif instr[4:10] == "0b001000":
        # Signed Extend Halfword
        return SxthT1
    elif instr[4:10] == "0b001001":
        # Signed Extend Byte
        return SxtbT1
    elif instr[4:10] == "0b001010":
        # Unsigned Extend Halfword
        return UxthT1
    elif instr[4:10] == "0b001011":
        # Unsigned Extend Byte
        return UxtbT1
    elif instr[4:8] == "0b0011":
        # Compare and Branch on Zero
        return CbzT1
    elif instr[4:7] == "0b010":
        # Push Multiple Registers
        return PushT1
    elif instr[4:11] == "0b0110010":
        # Set Endianness
        return SetendT1
    elif instr[4:11] == "0b0110011":
        # Change Processor State
        return CpsThumbT1
    elif instr[4:8] == "0b1001":
        # Compare and Branch on Zero
        return CbzT1
    elif instr[4:10] == "0b101000":
        # Byte-Reverse Word
        return RevT1
    elif instr[4:10] == "0b101001":
        # Byte-Reverse Packed Halfword
        return Rev16T1
    elif instr[4:10] == "0b101011":
        # Byte-Reverse Signed Halfword
        return RevshT1
    elif instr[4:8] == "0b1011":
        # Compare and Branch on Zero
        return CbzT1
    elif instr[4:7] == "0b110":
        # Pop Multiple Registers
        return PopThumbT1
    elif instr[4:8] == "0b1110":
        # Breakpoint
        return BkptT1
    elif instr[4:8] == "0b1111":
        #  If-Then, and hints
        return thumb_if_then_and_hints.decode_instruction(instr)
