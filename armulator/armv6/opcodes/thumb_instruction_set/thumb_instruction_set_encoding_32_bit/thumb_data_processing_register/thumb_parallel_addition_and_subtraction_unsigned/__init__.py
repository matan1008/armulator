from __future__ import absolute_import
from .uadd16_t1 import Uadd16T1
from .uasx_t1 import UasxT1
from .usax_t1 import UsaxT1
from .usub16_t1 import Usub16T1
from .uadd8_t1 import Uadd8T1
from .usub8_t1 import Usub8T1
from .uqadd16_t1 import Uqadd16T1
from .uqasx_t1 import UqasxT1
from .uqsax_t1 import UqsaxT1
from .uqsub16_t1 import Uqsub16T1
from .uqadd8_t1 import Uqadd8T1
from .uqsub8_t1 import Uqsub8T1
from .uhadd16_t1 import Uhadd16T1
from .uhasx_t1 import UhasxT1
from .uhsax_t1 import UhsaxT1
from .uhsub16_t1 import Uhsub16T1
from .uhadd8_t1 import Uhadd8T1
from .uhsub8_t1 import Uhsub8T1


def decode_instruction(instr):
    if instr[9:12] == "0b001" and instr[26:28] == "0b00":
        # Add 16-bit
        return Uadd16T1
    elif instr[9:12] == "0b010" and instr[26:28] == "0b00":
        # Add and Subtract with Exchange, 16-bit
        return UasxT1
    elif instr[9:12] == "0b110" and instr[26:28] == "0b00":
        # Subtract and Add with Exchange, 16-bit
        return UsaxT1
    elif instr[9:12] == "0b101" and instr[26:28] == "0b00":
        # Subtract 16-bit
        return Usub16T1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b00":
        # Add 8-bit
        return Uadd8T1
    elif instr[9:12] == "0b100" and instr[26:28] == "0b00":
        # Subtract 8-bit
        return Usub8T1
    elif instr[9:12] == "0b001" and instr[26:28] == "0b01":
        # Saturating Add 16-bit
        return Uqadd16T1
    elif instr[9:12] == "0b010" and instr[26:28] == "0b01":
        # Saturating Add and Subtract with Exchange, 16-bit
        return UqasxT1
    elif instr[9:12] == "0b110" and instr[26:28] == "0b01":
        # Saturating Subtract and Add with Exchange, 16-bit
        return UqsaxT1
    elif instr[9:12] == "0b101" and instr[26:28] == "0b01":
        # Saturating Subtract 16-bit
        return Uqsub16T1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b01":
        # Saturating Add 8-bit
        return Uqadd8T1
    elif instr[9:12] == "0b100" and instr[26:28] == "0b01":
        # Saturating Subtract 8-bit
        return Uqsub8T1
    elif instr[9:12] == "0b001" and instr[26:28] == "0b10":
        # Halving Add 16-bit
        return Uhadd16T1
    elif instr[9:12] == "0b010" and instr[26:28] == "0b10":
        # Halving Add and Subtract with Exchange, 16-bit
        return UhasxT1
    elif instr[9:12] == "0b110" and instr[26:28] == "0b10":
        # Halving Subtract and Add with Exchange, 16-bit
        return UhsaxT1
    elif instr[9:12] == "0b101" and instr[26:28] == "0b10":
        # Halving Subtract 16-bit
        return Uhsub16T1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b10":
        # Halving Add 8-bit
        return Uhadd8T1
    elif instr[9:12] == "0b100" and instr[26:28] == "0b10":
        # Halving Subtract 8-bit
        return Uhsub8T1
