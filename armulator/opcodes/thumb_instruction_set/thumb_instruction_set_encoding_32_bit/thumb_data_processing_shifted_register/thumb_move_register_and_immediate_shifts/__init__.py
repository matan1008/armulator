from mov_register_thumb_t3 import MovRegisterThumbT3
from lsl_immediate_t2 import LslImmediateT2
from lsr_immediate_t2 import LsrImmediateT2
from asr_immediate_t2 import AsrImmediateT2
from rrx_t1 import RrxT1
from ror_immediate_t1 import RorImmediateT1


def decode_instruction(instr):
    if instr[26:28] == "0b00" and instr[17:20] + instr[24:26] == "0b00000":
        # Move
        return MovRegisterThumbT3
    elif instr[26:28] == "0b00" and instr[17:20] + instr[24:26] != "0b00000":
        # Logical Shift Left
        return LslImmediateT2
    elif instr[26:28] == "0b01":
        # Logical Shift Right
        return LsrImmediateT2
    elif instr[26:28] == "0b10":
        # Arithmetic Shift Right
        return AsrImmediateT2
    elif instr[26:28] == "0b11" and instr[17:20] + instr[24:26] == "0b00000":
        # Rotate Right with Extend
        return RrxT1
    elif instr[26:28] == "0b11" and instr[17:20] + instr[24:26] != "0b00000":
        # Rotate Right
        return RorImmediateT1
