from __future__ import absolute_import
from .strex_a1 import StrexA1
from .ldrex_a1 import LdrexA1
from .strexd_a1 import StrexdA1
from .ldrexd_a1 import LdrexdA1
from .strexb_a1 import StrexbA1
from .ldrexb_a1 import LdrexbA1
from .strexh_a1 import StrexhA1
from .ldrexh_a1 import LdrexhA1


def decode_instruction(instr):
    if instr[8:12].uint == 0:
        # Swap Word, Swap Byte
        print("deprecated")
    elif instr[8:12] == "0b1000":
        # Store Register Exclusive
        return StrexA1
    elif instr[8:12] == "0b1001":
        # Load Register Exclusive
        return LdrexA1
    elif instr[8:12] == "0b1010":
        # Store Register Exclusive Doubleword
        return StrexdA1
    elif instr[8:12] == "0b1011":
        # Load Register Exclusive Doubleword
        return LdrexdA1
    elif instr[8:12] == "0b1100":
        # Store Register Exclusive Byte
        return StrexbA1
    elif instr[8:12] == "0b1101":
        # Load Register Exclusive Byte
        return LdrexbA1
    elif instr[8:12] == "0b1110":
        # Store Register Exclusive Halfword
        return StrexhA1
    elif instr[8:12] == "0b1111":
        # Load Register Exclusive Halfword
        return LdrexhA1
