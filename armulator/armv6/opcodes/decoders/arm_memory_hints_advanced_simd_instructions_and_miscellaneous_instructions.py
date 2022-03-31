from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.clrex_a1 import ClrexA1
from armulator.armv6.opcodes.concrete.cps_arm_a1 import CpsArmA1
from armulator.armv6.opcodes.concrete.dsb_a1 import DsbA1
from armulator.armv6.opcodes.concrete.isb_a1 import IsbA1
from armulator.armv6.opcodes.concrete.pld_immediate_a1 import PldImmediateA1
from armulator.armv6.opcodes.concrete.pld_literal_a1 import PldLiteralA1
from armulator.armv6.opcodes.concrete.pld_register_a1 import PldRegisterA1
from armulator.armv6.opcodes.concrete.setend_a1 import SetendA1


def decode_instruction(instr):
    op1 = substring(instr, 26, 20)
    instr_16 = bit_at(instr, 16)
    op2 = substring(instr, 7, 4)
    instr_26_25 = substring(instr, 26, 25)
    instr_26_24 = substring(instr, 26, 24)
    instr_22_20 = substring(instr, 22, 20)
    instr_21_20 = substring(instr, 21, 20)
    rn = substring(instr, 19, 16)
    instr_4 = bit_at(instr, 4)
    if op1 == 0b0010000 and not bit_at(instr, 5) and not instr_16:
        # Change Processor State
        return CpsArmA1
    elif op1 == 0b0010000 and op2 == 0b0000 and instr_16:
        # Set Endianness
        return SetendA1
    elif instr_26_25 == 0b01:
        # v7 variant, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b100 and not bit_at(instr, 20):
        # v7 variant, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b100 and instr_22_20 == 0b001:
        # MP extension, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b100 and instr_22_20 == 0b101:
        # v7 variant, will not be implemented
        # Preload Instruction
        raise NotImplementedError()
    elif instr_26_24 == 0b100 and instr_21_20 == 0b11:
        print('unpredictable')
    elif instr_26_24 == 0b101 and instr_22_20 == 0b001 and rn != 0b1111:
        # MP extension, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b101 and instr_22_20 == 0b001 and rn == 0b1111:
        print('unpredictable')
    elif instr_26_24 == 0b101 and instr_22_20 == 0b101 and rn != 0b1111:
        # Preload Data
        return PldImmediateA1
    elif instr_26_24 == 0b101 and instr_22_20 == 0b101 and rn == 0b1111:
        # Preload Data
        return PldLiteralA1
    elif op1 == 0b1010011:
        print('unpredictable')
    elif op1 == 0b1010111 and op2 == 0b0000:
        print('unpredictable')
    elif op1 == 0b1010111 and op2 == 0b0001:
        # Clear-Exclusive
        return ClrexA1
    elif op1 == 0b1010111 and substring(instr, 7, 5) == 0b001:
        print('unpredictable')
    elif op1 == 0b1010111 and op2 == 0b0100:
        # Data Synchronization Barrier
        return DsbA1
    elif op1 == 0b1010111 and op2 == 0b0101:
        # v7 variant, will not be implemented
        raise NotImplementedError()
    elif op1 == 0b1010111 and op2 == 0b0110:
        # Instruction Synchronization Barrier
        return IsbA1
    elif op1 == 0b1010111 and op2 == 0b0111:
        print('unpredictable')
    elif op1 == 0b1010111 and bit_at(instr, 7):
        print('unpredictable')
    elif substring(instr, 26, 23) == 0b1011 and instr_21_20 == 0b11:
        print('unpredictable')
    elif instr_26_24 == 0b110 and instr_22_20 == 0b001 and not instr_4:
        # MP extension, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b110 and instr_22_20 == 0b101 and not instr_4:
        # v7 variant, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b111 and instr_22_20 == 0b001 and not instr_4:
        # MP extension, will not be implemented
        raise NotImplementedError()
    elif instr_26_24 == 0b111 and instr_22_20 == 0b101 and not instr_4:
        # Preload Data
        return PldRegisterA1
    elif instr_26_25 == 0b11 and instr_21_20 == 0b11 and not instr_4:
        print('unpredictable')
    elif op1 == 0b1111111 and op2 == 0b1111:
        raise UndefinedInstructionException()
