from __future__ import absolute_import
from .sadd16_a1 import Sadd16A1
from .sasx_a1 import SasxA1
from .ssax_a1 import SsaxA1
from .ssub16_a1 import Ssub16A1
from .sadd8_a1 import Sadd8A1
from .ssub8_a1 import Ssub8A1
from .qadd16_a1 import Qadd16A1
from .qasx_a1 import QasxA1
from .qsax_a1 import QsaxA1
from .qsub16_a1 import Qsub16A1
from .qadd8_a1 import Qadd8A1
from .qsub8_a1 import Qsub8A1
from .shadd16_a1 import Shadd16A1
from .shasx_a1 import ShasxA1
from .shsax_a1 import ShsaxA1
from .shsub16_a1 import Shsub16A1
from .shadd8_a1 import Shadd8A1
from .shsub8_a1 import Shsub8A1


def decode_instruction(instr):
    if instr[10:12] == "0b01" and instr[24:27] == "0b000":
        # Add 16-bit
        return Sadd16A1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b001":
        # Add and Subtract with Exchange, 16-bit
        return SasxA1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b010":
        # Subtract and Add with Exchange, 16-bit
        return SsaxA1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b011":
        # Subtract 16-bit
        return Ssub16A1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b100":
        # Add 8-bit
        return Sadd8A1
    elif instr[10:12] == "0b01" and instr[24:27] == "0b111":
        # Subtract 8-bit
        return Ssub8A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b000":
        # Saturating Add 16-bit
        return Qadd16A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b001":
        # Saturating Add and Subtract with Exchange, 16-bit
        return QasxA1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b010":
        # Saturating Subtract and Add with Exchange, 16-bit
        return QsaxA1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b011":
        # Saturating Subtract 16-bit
        return Qsub16A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b100":
        # Saturating Add 8-bit
        return Qadd8A1
    elif instr[10:12] == "0b10" and instr[24:27] == "0b111":
        # Saturating Subtract 8-bit
        return Qsub8A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b000":
        # Halving Add 16-bit
        return Shadd16A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b001":
        # Halving Add and Subtract with Exchange, 16-bit
        return ShasxA1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b010":
        # Halving Subtract and Add with Exchange, 16-bit
        return ShsaxA1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b011":
        # Halving Subtract 16-bit
        return Shsub16A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b100":
        # Halving Add 8-bit
        return Shadd8A1
    elif instr[10:12] == "0b11" and instr[24:27] == "0b111":
        # Halving Subtract 8-bit
        return Shsub8A1
