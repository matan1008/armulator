from __future__ import absolute_import
from .uadd16_a1 import Uadd16A1
from .uasx_a1 import UasxA1
from .usax_a1 import UsaxA1
from .usub16_a1 import Usub16A1
from .uadd8_a1 import Uadd8A1
from .usub8_a1 import Usub8A1
from .uqadd16_a1 import Uqadd16A1
from .uqasx_a1 import UqasxA1
from .uqsax_a1 import UqsaxA1
from .uqsub16_a1 import Uqsub16A1
from .uqadd8_a1 import Uqadd8A1
from .uqsub8_a1 import Uqsub8A1
from .uhadd16_a1 import Uhadd16A1
from .uhasx_a1 import UhasxA1
from .uhsax_a1 import UhsaxA1
from .uhsub16_a1 import Uhsub16A1
from .uhadd8_a1 import Uhadd8A1
from .uhsub8_a1 import Uhsub8A1


def decode_instruction(instr):
    if instr[10:12] == "0b01" and instr[24:27] == "0b000":
        # Add 16-bit
        return Uadd16A1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b001":
        # Add and Subtract with Exchange, 16-bit
        return UasxA1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b010":
        # Subtract and Add with Exchange, 16-bit
        return UsaxA1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b011":
        # Subtract 16-bit
        return Usub16A1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b100":
        # Add 8-bit
        return Uadd8A1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b111":
        # Subtract 8-bit
        return Usub8A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b000":
        # Saturating Add 16-bit
        return Uqadd16A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b001":
        # Saturating Add and Subtract with Exchange, 16-bit
        return UqasxA1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b010":
        # Saturating Subtract and Add with Exchange, 16-bit
        return UqsaxA1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b011":
        # Saturating Subtract 16-bit
        return Uqsub16A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b100":
        # Saturating Add 8-bit
        return Uqadd8A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b111":
        # Saturating Subtract 8-bit
        return Uqsub8A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b000":
        # Halving Add 16-bit
        return Uhadd16A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b001":
        # Halving Add and Subtract with Exchange, 16-bit
        return UhasxA1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b010":
        # Halving Subtract and Add with Exchange, 16-bit
        return UhsaxA1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b011":
        # Halving Subtract 16-bit
        return Uhsub16A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b100":
        # Halving Add 8-bit
        return Uhadd8A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b111":
        # Halving Subtract 8-bit
        return Uhsub8A1
