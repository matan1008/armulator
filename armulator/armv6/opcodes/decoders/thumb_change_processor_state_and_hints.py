from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.cps_thumb_t2 import CpsThumbT2
from armulator.armv6.opcodes.concrete.nop_t2 import NopT2
from armulator.armv6.opcodes.concrete.sev_t2 import SevT2
from armulator.armv6.opcodes.concrete.wfe_t2 import WfeT2
from armulator.armv6.opcodes.concrete.wfi_t2 import WfiT2
from armulator.armv6.opcodes.concrete.yield_t2 import YieldT2


def decode_instruction(instr):
    instr_op1 = substring(instr, 10, 8)
    instr_op2 = substring(instr, 7, 0)
    if instr_op1 != 0b000:
        # Change Processor State
        return CpsThumbT2
    elif instr_op2 == 0b00000000:
        # No Operation hint
        return NopT2
    elif instr_op2 == 0b00000001:
        # Yield hint
        return YieldT2
    elif instr_op2 == 0b00000010:
        # Wait For Event hint
        return WfeT2
    elif instr_op2 == 0b00000011:
        # Wait For Interrupt hint
        return WfiT2
    elif instr_op2 == 0b00000100:
        # Send Event hint
        return SevT2
    elif substring(instr, 7, 4) == 0b1111:
        # Debug hint
        # armv7, will not be implemented
        raise NotImplementedError()
