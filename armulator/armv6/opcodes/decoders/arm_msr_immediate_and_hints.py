from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.msr_immediate_application_a1 import MsrImmediateApplicationA1
from armulator.armv6.opcodes.concrete.msr_immediate_system_a1 import MsrImmediateSystemA1
from armulator.armv6.opcodes.concrete.nop_a1 import NopA1
from armulator.armv6.opcodes.concrete.sev_a1 import SevA1
from armulator.armv6.opcodes.concrete.wfe_a1 import WfeA1
from armulator.armv6.opcodes.concrete.wfi_a1 import WfiA1
from armulator.armv6.opcodes.concrete.yield_a1 import YieldA1


def decode_instruction(instr):
    op = bit_at(instr, 22)
    op1 = substring(instr, 19, 16)
    op2 = substring(instr, 7, 0)
    if not op and op1 == 0b0000 and op2 == 0b00000000:
        # No Operation hint
        return NopA1
    elif not op and op1 == 0b0000 and op2 == 0b00000001:
        # Yield hint
        return YieldA1
    elif not op and op1 == 0b0000 and op2 == 0b00000010:
        # Wait For Event hint
        return WfeA1
    elif not op and op1 == 0b0000 and op2 == 0b00000011:
        # Wait For Interrupt hint
        return WfiA1
    elif not op and op1 == 0b0000 and op2 == 0b00000100:
        # Send Event hint
        return SevA1
    elif not op and op1 == 0b0000 and substring(instr, 7, 4) == 0b1111:
        # Debug hint
        raise NotImplementedError()
    elif not op and (op1 == 0b0100 or (bit_at(instr, 19) and substring(instr, 17, 16) == 0b00)):
        # Move to Special register, Application level
        return MsrImmediateApplicationA1
    elif op or (not op and (bit_at(instr, 17) or substring(instr, 17, 16) == 0b01)):
        # Move to Special register, System level
        return MsrImmediateSystemA1
