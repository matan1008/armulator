from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.add_sp_plus_immediate_t2 import AddSpPlusImmediateT2
from armulator.armv6.opcodes.concrete.bkpt_t1 import BkptT1
from armulator.armv6.opcodes.concrete.cbz_t1 import CbzT1
from armulator.armv6.opcodes.concrete.cps_thumb_t1 import CpsThumbT1
from armulator.armv6.opcodes.concrete.pop_thumb_t1 import PopThumbT1
from armulator.armv6.opcodes.concrete.push_t1 import PushT1
from armulator.armv6.opcodes.concrete.rev16_t1 import Rev16T1
from armulator.armv6.opcodes.concrete.rev_t1 import RevT1
from armulator.armv6.opcodes.concrete.revsh_t1 import RevshT1
from armulator.armv6.opcodes.concrete.setend_t1 import SetendT1
from armulator.armv6.opcodes.concrete.sub_sp_minus_immediate_t1 import SubSpMinusImmediateT1
from armulator.armv6.opcodes.concrete.sxtb_t1 import SxtbT1
from armulator.armv6.opcodes.concrete.sxth_t1 import SxthT1
from armulator.armv6.opcodes.concrete.uxtb_t1 import UxtbT1
from armulator.armv6.opcodes.concrete.uxth_t1 import UxthT1
from armulator.armv6.opcodes.decoders import thumb_if_then_and_hints


def decode_instruction(instr):
    if substring(instr, 11, 7) == 0b00000:
        # Add Immediate to SP
        return AddSpPlusImmediateT2
    elif substring(instr, 11, 7) == 0b00001:
        # Subtract Immediate from SP
        return SubSpMinusImmediateT1
    elif substring(instr, 11, 8) == 0b0001:
        # Compare and Branch on Zero
        return CbzT1
    elif substring(instr, 11, 6) == 0b001000:
        # Signed Extend Halfword
        return SxthT1
    elif substring(instr, 11, 6) == 0b001001:
        # Signed Extend Byte
        return SxtbT1
    elif substring(instr, 11, 6) == 0b001010:
        # Unsigned Extend Halfword
        return UxthT1
    elif substring(instr, 11, 6) == 0b001011:
        # Unsigned Extend Byte
        return UxtbT1
    elif substring(instr, 11, 8) == 0b0011:
        # Compare and Branch on Zero
        return CbzT1
    elif substring(instr, 11, 9) == 0b010:
        # Push Multiple Registers
        return PushT1
    elif substring(instr, 11, 5) == 0b0110010:
        # Set Endianness
        return SetendT1
    elif substring(instr, 11, 5) == 0b0110011:
        # Change Processor State
        return CpsThumbT1
    elif substring(instr, 11, 8) == 0b1001:
        # Compare and Branch on Zero
        return CbzT1
    elif substring(instr, 11, 6) == 0b101000:
        # Byte-Reverse Word
        return RevT1
    elif substring(instr, 11, 6) == 0b101001:
        # Byte-Reverse Packed Halfword
        return Rev16T1
    elif substring(instr, 11, 6) == 0b101011:
        # Byte-Reverse Signed Halfword
        return RevshT1
    elif substring(instr, 11, 8) == 0b1011:
        # Compare and Branch on Zero
        return CbzT1
    elif substring(instr, 11, 9) == 0b110:
        # Pop Multiple Registers
        return PopThumbT1
    elif substring(instr, 11, 8) == 0b1110:
        # Breakpoint
        return BkptT1
    elif substring(instr, 11, 8) == 0b1111:
        #  If-Then, and hints
        return thumb_if_then_and_hints.decode_instruction(instr)
