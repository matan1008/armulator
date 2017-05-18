from mov_register_thumb_t2 import MovRegisterThumbT2
from lsl_immediate_t1 import LslImmediateT1
from lsr_immediate_t1 import LsrImmediateT1
from asr_immediate_t1 import AsrImmediateT1
from add_register_thumb_t1 import AddRegisterThumbT1
from sub_register_t1 import SubRegisterT1
from add_immediate_thumb_t1 import AddImmediateThumbT1
from sub_immediate_thumb_t1 import SubImmediateThumbT1
from mov_immediate_t1 import MovImmediateT1
from cmp_immediate_t1 import CmpImmediateT1
from add_immediate_thumb_t2 import AddImmediateThumbT2
from sub_immediate_thumb_t2 import SubImmediateThumbT2


def decode_instruction(instr):
    if instr[2:5] == "0b000":
        # Logical Shift Left
        if instr[5:10] == "0b00000":
            return MovRegisterThumbT2
        else:
            return LslImmediateT1
    elif instr[2:5] == "0b001":
        # Logical Shift Right
        return LsrImmediateT1
    elif instr[2:5] == "0b010":
        # Arithmetic Shift Right
        return AsrImmediateT1
    elif instr[2:7] == "0b01100":
        # Add register
        return AddRegisterThumbT1
    elif instr[2:7] == "0b01101":
        # Subtract register
        return SubRegisterT1
    elif instr[2:7] == "0b01110":
        # Add 3-bit immediate
        return AddImmediateThumbT1
    elif instr[2:7] == "0b01111":
        # Subtract 3-bit immediate
        return SubImmediateThumbT1
    elif instr[2:5] == "0b100":
        # Move
        return MovImmediateT1
    elif instr[2:5] == "0b101":
        # Compare
        return CmpImmediateT1
    elif instr[2:5] == "0b110":
        # Add 8-bit immediate
        return AddImmediateThumbT2
    elif instr[2:5] == "0b111":
        # Subtract 8-bit immediate
        return SubImmediateThumbT2
