from __future__ import absolute_import
from .it_t1 import ItT1
from .nop_t1 import NopT1
from .yield_t1 import YieldT1
from .wfe_t1 import WfeT1
from .wfi_t1 import WfiT1
from .sev_t1 import SevT1


def decode_instruction(instr):
    if instr[12:16] != "0b0000":
        # If-Then
        return ItT1
    elif instr[12:16] == "0b0000" and instr[8:12] == "0b0000":
        # No Operation hint
        return NopT1
    elif instr[12:16] == "0b0000" and instr[8:12] == "0b0001":
        # Yield hint
        return YieldT1
    elif instr[12:16] == "0b0000" and instr[8:12] == "0b0010":
        # Wait For Event hint
        return WfeT1
    elif instr[12:16] == "0b0000" and instr[8:12] == "0b0011":
        # Wait For Interrupt hint
        return WfiT1
    elif instr[12:16] == "0b0000" and instr[8:12] == "0b0100":
        # Send Event hint
        return SevT1
