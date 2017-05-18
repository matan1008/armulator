from smla_a1 import SmlaA1
from smlaw_a1 import SmlawA1
from smulw_a1 import SmulwA1
from smlalxy_a1 import SmlalxyA1
from smul_a1 import SmulA1


def decode_instruction(instr):
    if instr[9:11] == "0b00":
        # Signed 16-bit multiply, 32-bit accumulate
        return SmlaA1
    elif instr[9:11] == "0b01" and not instr[26]:
        # Signed 16-bit X 32-bit multiply, 32-bit accumulate
        return SmlawA1
    elif instr[9:11] == "0b01" and instr[26]:
        # Signed 16-bit X 32-bit multiply, 32-bit result
        return SmulwA1
    elif instr[9:11] == "0b10":
        # Signed 16-bit multiply, 64-bit accumulate
        return SmlalxyA1
    elif instr[9:11] == "0b11":
        # Signed 16-bit multiply, 64-bit result
        return SmulA1
