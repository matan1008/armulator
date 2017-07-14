from cps_thumb_t2 import CpsThumbT2
from nop_t2 import NopT2
from yield_t2 import YieldT2
from wfe_t2 import WfeT2
from wfi_t2 import WfiT2
from sev_t2 import SevT2


def decode_instruction(instr):
    if instr[21:24] != "0b000":
        # Change Processor State
        return CpsThumbT2
    elif instr[21:24] == "0b000" and instr[24:32] == "0b00000000":
        # No Operation hint
        return NopT2
    elif instr[21:24] == "0b000" and instr[24:32] == "0b00000001":
        # Yield hint
        return YieldT2
    elif instr[21:24] == "0b000" and instr[24:32] == "0b00000010":
        # Wait For Event hint
        return WfeT2
    elif instr[21:24] == "0b000" and instr[24:32] == "0b00000011":
        # Wait For Interrupt hint
        return WfiT2
    elif instr[21:24] == "0b000" and instr[24:32] == "0b00000100":
        # Send Event hint
        return SevT2
    elif instr[21:24] == "0b000" and instr[24:28] == "0b1111":
        # Debug hint
        # armv7, will not be implemented
        raise NotImplementedError()
