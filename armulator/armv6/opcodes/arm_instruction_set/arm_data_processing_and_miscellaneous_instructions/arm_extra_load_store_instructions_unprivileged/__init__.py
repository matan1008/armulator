from __future__ import absolute_import
from .strht_a1 import StrhtA1
from .strht_a2 import StrhtA2
from .ldrht_a1 import LdrhtA1
from .ldrht_a2 import LdrhtA2
from .ldrsbt_a1 import LdrsbtA1
from .ldrsbt_a2 import LdrsbtA2
from .ldrsht_a1 import LdrshtA1
from .ldrsht_a2 import LdrshtA2


def decode_instruction(instr):
    if instr[25:27] == "0b01" and not instr[11]:
        # Store Halfword Unprivileged
        if instr[9]:
            return StrhtA1
        else:
            return StrhtA2
    elif instr[25:27] == "0b01" and instr[11]:
        # Load Halfword Unprivileged
        if instr[9]:
            return LdrhtA1
        else:
            return LdrhtA2
    elif instr[25:27] == "0b10" and instr[11]:
        # Load Signed Byte Unprivileged
        if instr[9]:
            return LdrsbtA1
        else:
            return LdrsbtA2
    elif instr[25:27] == "0b11" and instr[11]:
        # Load Signed Halfword Unprivileged
        if instr[9]:
            return LdrshtA1
        else:
            return LdrshtA2
