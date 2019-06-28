from __future__ import absolute_import
from .enterx_t1 import EnterxT1
from .clrex_t1 import ClrexT1
from .dsb_t1 import DsbT1
from .isb_t1 import IsbT1


def decode_instruction(instr):
    if instr[24:28] == "0b0000" or instr[24:28] == "0b0001":
        # Exit ThumbEE state / Enter ThumbEE state
        return EnterxT1
    elif instr[24:28] == "0b0010":
        # Clear-Exclusive
        return ClrexT1
    elif instr[24:28] == "0b0100":
        # Data Synchronization Barrier
        return DsbT1
    elif instr[24:28] == "0b0101":
        # Data Memory Barrier
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr[24:28] == "0b0110":
        # Instruction Synchronization Barrier
        return IsbT1
