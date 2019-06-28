from __future__ import absolute_import
from .sadd16_t1 import Sadd16T1
from .sasx_t1 import SasxT1
from .ssax_t1 import SsaxT1
from .ssub16_t1 import Ssub16T1
from .sadd8_t1 import Sadd8T1
from .ssub8_t1 import Ssub8T1
from .qadd16_t1 import Qadd16T1
from .qasx_t1 import QasxT1
from .qsax_t1 import QsaxT1
from .qsub16_t1 import Qsub16T1
from .qadd8_t1 import Qadd8T1
from .qsub8_t1 import Qsub8T1
from .shadd16_t1 import Shadd16T1
from .shasx_t1 import ShasxT1
from .shsax_t1 import ShsaxT1
from .shsub16_t1 import Shsub16T1
from .shadd8_t1 import Shadd8T1
from .shsub8_t1 import Shsub8T1


def decode_instruction(instr):
    if instr[9:12] == "0b001" and instr[26:28] == "0b00":
        # Add 16-bit
        return Sadd16T1
    elif instr[9:12] == "0b010" and instr[26:28] == "0b00":
        # Add and Subtract with Exchange, 16-bit
        return SasxT1
    elif instr[9:12] == "0b110" and instr[26:28] == "0b00":
        # Subtract and Add with Exchange, 16-bit
        return SsaxT1
    elif instr[9:12] == "0b101" and instr[26:28] == "0b00":
        # Subtract 16-bit
        return Ssub16T1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b00":
        # Add 8-bit
        return Sadd8T1
    elif instr[9:12] == "0b100" and instr[26:28] == "0b00":
        # Subtract 8-bit
        return Ssub8T1
    elif instr[9:12] == "0b001" and instr[26:28] == "0b01":
        # Saturating Add 16-bit
        return Qadd16T1
    elif instr[9:12] == "0b010" and instr[26:28] == "0b01":
        # Saturating Add and Subtract with Exchange, 16-bit
        return QasxT1
    elif instr[9:12] == "0b110" and instr[26:28] == "0b01":
        # Saturating Subtract and Add with Exchange, 16-bit
        return QsaxT1
    elif instr[9:12] == "0b101" and instr[26:28] == "0b01":
        # Saturating Subtract 16-bit
        return Qsub16T1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b01":
        # Saturating Add 8-bit
        return Qadd8T1
    elif instr[9:12] == "0b100" and instr[26:28] == "0b01":
        # Saturating Subtract 8-bit
        return Qsub8T1
    elif instr[9:12] == "0b001" and instr[26:28] == "0b10":
        # Halving Add 16-bit
        return Shadd16T1
    elif instr[9:12] == "0b010" and instr[26:28] == "0b10":
        # Halving Add and Subtract with Exchange, 16-bit
        return ShasxT1
    elif instr[9:12] == "0b110" and instr[26:28] == "0b10":
        # Halving Subtract and Add with Exchange, 16-bit
        return ShsaxT1
    elif instr[9:12] == "0b101" and instr[26:28] == "0b10":
        # Halving Subtract 16-bit
        return Shsub16T1
    elif instr[9:12] == "0b000" and instr[26:28] == "0b10":
        # Halving Add 8-bit
        return Shadd8T1
    elif instr[9:12] == "0b100" and instr[26:28] == "0b10":
        # Halving Subtract 8-bit
        return Shsub8T1
