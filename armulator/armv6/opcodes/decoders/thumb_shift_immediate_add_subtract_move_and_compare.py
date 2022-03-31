from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t1 import AddImmediateThumbT1
from armulator.armv6.opcodes.concrete.add_immediate_thumb_t2 import AddImmediateThumbT2
from armulator.armv6.opcodes.concrete.add_register_thumb_t1 import AddRegisterThumbT1
from armulator.armv6.opcodes.concrete.asr_immediate_t1 import AsrImmediateT1
from armulator.armv6.opcodes.concrete.cmp_immediate_t1 import CmpImmediateT1
from armulator.armv6.opcodes.concrete.lsl_immediate_t1 import LslImmediateT1
from armulator.armv6.opcodes.concrete.lsr_immediate_t1 import LsrImmediateT1
from armulator.armv6.opcodes.concrete.mov_immediate_t1 import MovImmediateT1
from armulator.armv6.opcodes.concrete.mov_register_thumb_t2 import MovRegisterThumbT2
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t1 import SubImmediateThumbT1
from armulator.armv6.opcodes.concrete.sub_immediate_thumb_t2 import SubImmediateThumbT2
from armulator.armv6.opcodes.concrete.sub_register_t1 import SubRegisterT1


def decode_instruction(instr):
    if substring(instr, 13, 11) == 0b000:
        # Logical Shift Left
        if substring(instr, 10, 6) == 0b00000:
            return MovRegisterThumbT2
        else:
            return LslImmediateT1
    elif substring(instr, 13, 11) == 0b001:
        # Logical Shift Right
        return LsrImmediateT1
    elif substring(instr, 13, 11) == 0b010:
        # Arithmetic Shift Right
        return AsrImmediateT1
    elif substring(instr, 13, 9) == 0b01100:
        # Add register
        return AddRegisterThumbT1
    elif substring(instr, 13, 9) == 0b01101:
        # Subtract register
        return SubRegisterT1
    elif substring(instr, 13, 9) == 0b01110:
        # Add 3-bit immediate
        return AddImmediateThumbT1
    elif substring(instr, 13, 9) == 0b01111:
        # Subtract 3-bit immediate
        return SubImmediateThumbT1
    elif substring(instr, 13, 11) == 0b100:
        # Move
        return MovImmediateT1
    elif substring(instr, 13, 11) == 0b101:
        # Compare
        return CmpImmediateT1
    elif substring(instr, 13, 11) == 0b110:
        # Add 8-bit immediate
        return AddImmediateThumbT2
    elif substring(instr, 13, 11) == 0b111:
        # Subtract 8-bit immediate
        return SubImmediateThumbT2
