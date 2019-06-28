from __future__ import absolute_import
from .b_t1 import BT1
from .udf_t1 import UdfT1
from .svc_t1 import SvcT1


def decode_instruction(instr):
    if instr[4:7] != "0b111":
        # Conditional branch
        return BT1
    elif instr[4:8] == "0b1110":
        # Permanently UNDEFINED
        return UdfT1
    elif instr[4:8] == "0b1111":
        # Supervisor Call
        return SvcT1
