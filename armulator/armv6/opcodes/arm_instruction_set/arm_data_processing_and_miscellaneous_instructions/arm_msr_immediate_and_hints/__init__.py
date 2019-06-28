from __future__ import absolute_import
from .nop_a1 import NopA1
from .yield_a1 import YieldA1
from .wfe_a1 import WfeA1
from .wfi_a1 import WfiA1
from .sev_a1 import SevA1
from .msr_immediate_application_a1 import MsrImmediateApplicationA1
from .msr_immediate_system_a1 import MsrImmediateSystemA1


def decode_instruction(instr):
    if not instr[9] and instr[12:16] == "0b0000" and instr[24:32] == "0b00000000":
        # No Operation hint
        return NopA1
    elif not instr[9] and instr[12:16] == "0b0000" and instr[24:32] == "0b00000001":
        # Yield hint
        return YieldA1
    elif not instr[9] and instr[12:16] == "0b0000" and instr[24:32] == "0b00000010":
        # Wait For Event hint
        return WfeA1
    elif not instr[9] and instr[12:16] == "0b0000" and instr[24:32] == "0b00000011":
        # Wait For Interrupt hint
        return WfiA1
    elif not instr[9] and instr[12:16] == "0b0000" and instr[24:32] == "0b00000100":
        # Send Event hint
        return SevA1
    elif not instr[9] and instr[12:16] == "0b0000" and instr[24:28] == "0b1111":
        # Debug hint
        raise NotImplementedError()
    elif not instr[9] and (instr[12:16] == "0b0100" or (instr[12:13] + instr[14:16]) == "0b100"):
        # Move to Special register, Application level
        return MsrImmediateApplicationA1
    elif instr[9] or (not instr[9] and (instr[14] or instr[14:16] == "0b01")):
        # Move to Special register, System level
        return MsrImmediateSystemA1
