from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.bkpt_a1 import BkptA1
from armulator.armv6.opcodes.concrete.blx_register_a1 import BlxRegisterA1
from armulator.armv6.opcodes.concrete.bx_a1 import BxA1
from armulator.armv6.opcodes.concrete.bxj_a1 import BxjA1
from armulator.armv6.opcodes.concrete.clz_a1 import ClzA1
from armulator.armv6.opcodes.concrete.mrs_application_a1 import MrsApplicationA1
from armulator.armv6.opcodes.concrete.mrs_system_a1 import MrsSystemA1
from armulator.armv6.opcodes.concrete.msr_register_application_a1 import MsrRegisterApplicationA1
from armulator.armv6.opcodes.concrete.msr_register_system_a1 import MsrRegisterSystemA1
from armulator.armv6.opcodes.concrete.smc_a1 import SmcA1
from armulator.armv6.opcodes.decoders import arm_saturating_addition_and_subtraction


def decode_instruction(instr):
    op2 = substring(instr, 6, 4)
    op = substring(instr, 22, 21)
    b = bit_at(instr, 9)
    instr_21 = bit_at(instr, 21)
    if op2 == 0b000 and b and not instr_21:
        # Move from Banked or Special register, ARMv7VE Only
        raise NotImplementedError()
    elif op2 == 0b000 and b and instr_21:
        # Move to Banked or Special register, ARMv7VE Only
        raise NotImplementedError()
    elif op2 == 0b000 and not b and not instr_21:
        # Move from Special register
        if not bit_at(instr, 22):
            return MrsApplicationA1
        else:
            return MrsSystemA1
    elif op2 == 0b000 and not b and op == 0b01 and substring(instr, 17, 16) == 0b00:
        # Move to Special register, Application level
        return MsrRegisterApplicationA1
    elif op2 == 0b000 and not b and op == 0b01 and (substring(instr, 17, 16) == 0b01 or bit_at(instr, 17)):
        # Move to Special register, System level
        return MsrRegisterSystemA1
    elif op2 == 0b000 and not b and op == 0b11:
        # Move to Special register, System level
        return MsrRegisterSystemA1
    elif op2 == 0b001 and op == 0b01:
        # Branch and Exchange
        return BxA1
    elif op2 == 0b001 and op == 0b11:
        # Count Leading Zeros
        return ClzA1
    elif op2 == 0b010 and op == 0b01:
        # Branch and Exchange Jazelle
        return BxjA1
    elif op2 == 0b011 and op == 0b01:
        # Branch with Link and Exchange
        return BlxRegisterA1
    elif op2 == 0b101:
        return arm_saturating_addition_and_subtraction.decode_instruction(instr)
    elif op2 == 0b110 and op == 0b11:
        # Exception Return, ARMv7VE
        raise NotImplementedError()
    elif op2 == 0b111 and op == 0b01:
        # Breakpoint
        return BkptA1
    elif op2 == 0b111 and op == 0b10:
        # Hypervisor Call, ARMv7VE
        raise NotImplementedError()
    elif op2 == 0b111 and op == 0b11:
        # Secure Monitor Call
        return SmcA1
