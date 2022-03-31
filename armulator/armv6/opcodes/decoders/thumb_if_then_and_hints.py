from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.it_t1 import ItT1
from armulator.armv6.opcodes.concrete.nop_t1 import NopT1
from armulator.armv6.opcodes.concrete.yield_t1 import YieldT1
from armulator.armv6.opcodes.concrete.sev_t1 import SevT1
from armulator.armv6.opcodes.concrete.wfe_t1 import WfeT1
from armulator.armv6.opcodes.concrete.wfi_t1 import WfiT1


def decode_instruction(instr):
    if substring(instr, 3, 0) != 0b0000:
        # If-Then
        return ItT1
    elif substring(instr, 3, 0) == 0b0000 and substring(instr, 7, 4) == 0b0000:
        # No Operation hint
        return NopT1
    elif substring(instr, 3, 0) == 0b0000 and substring(instr, 7, 4) == 0b0001:
        # Yield hint
        return YieldT1
    elif substring(instr, 3, 0) == 0b0000 and substring(instr, 7, 4) == 0b0010:
        # Wait For Event hint
        return WfeT1
    elif substring(instr, 3, 0) == 0b0000 and substring(instr, 7, 4) == 0b0011:
        # Wait For Interrupt hint
        return WfiT1
    elif substring(instr, 3, 0) == 0b0000 and substring(instr, 7, 4) == 0b0100:
        # Send Event hint
        return SevT1
