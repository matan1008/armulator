from __future__ import absolute_import
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from .cps_arm_a1 import CpsArmA1
from .setend_a1 import SetendA1
from .pld_immediate_a1 import PldImmediateA1
from .pld_literal_a1 import PldLiteralA1
from .clrex_a1 import ClrexA1
from .dsb_a1 import DsbA1
from .isb_a1 import IsbA1
from .pld_register_a1 import PldRegisterA1


def decode_instruction(instr):
    if instr[5:12] == "0b0010000" and not instr[26] and not instr[15]:
        # Change Processor State
        return CpsArmA1
    elif instr[5:12] == "0b0010000" and instr[24:28] == "0b0000" and instr[15]:
        # Set Endianness
        return SetendA1
    elif instr[5:12] == "0b0010010" and instr[24:28] == "0b0111":
        print("unpredictable")
    elif instr[5:7] == "0b01":
        # v7 variant, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b100" and not instr[11]:
        # v7 variant, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b100" and instr[9:12] == "0b001":
        # MP extension, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b100" and instr[9:12] == "0b101":
        # v7 variant, will not be impelemented
        # Preload Instruction
        raise NotImplementedError()
    elif instr[5:8] == "0b100" and instr[10:12] == "0b11":
        print("unpredictable")
    elif instr[5:8] == "0b101" and instr[9:12] == "0b001" and instr[12:16] != "0b1111":
        # MP extension, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b101" and instr[9:12] == "0b001" and instr[12:16] == "0b1111":
        print("unpredictable")
    elif instr[5:8] == "0b101" and instr[9:12] == "0b101" and instr[12:16] != "0b1111":
        # Preload Data
        return PldImmediateA1
    elif instr[5:8] == "0b101" and instr[9:12] == "0b101" and instr[12:16] == "0b1111":
        # Preload Data
        return PldLiteralA1
    elif instr[5:12] == "0b1010011":
        print("unpredictable")
    elif instr[5:12] == "0b1010111" and instr[24:28] == "0b0000":
        print("unpredictable")
    elif instr[5:12] == "0b1010111" and instr[24:28] == "0b0001":
        # Clear-Exclusive
        return ClrexA1
    elif instr[5:12] == "0b1010111" and instr[24:27] == "0b001":
        print("unpredictable")
    elif instr[5:12] == "0b1010111" and instr[24:28] == "0b0100":
        # Data Synchronization Barrier
        return DsbA1
    elif instr[5:12] == "0b1010111" and instr[24:28] == "0b0101":
        # v7 variant, will not be impelemented
        raise NotImplementedError()
    elif instr[5:12] == "0b1010111" and instr[24:28] == "0b0110":
        # Instruction Synchronization Barrier
        return IsbA1
    elif instr[5:12] == "0b1010111" and instr[24:28] == "0b0111":
        print("unpredictable")
    elif instr[5:12] == "0b1010111" and instr[24]:
        print("unpredictable")
    elif instr[5:9] == "0b1011" and instr[10:12] == "0b11":
        print("unpredictable")
    elif instr[5:8] == "0b110" and instr[9:12] == "0b001" and not instr[27]:
        # MP extension, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b110" and instr[9:12] == "0b101" and not instr[27]:
        # v7 variant, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b111" and instr[9:12] == "0b001" and not instr[27]:
        # MP extension, will not be impelemented
        raise NotImplementedError()
    elif instr[5:8] == "0b111" and instr[9:12] == "0b101" and not instr[27]:
        # Preload Data
        return PldRegisterA1
    elif instr[5:7] == "0b11" and instr[10:12] == "0b11":
        print("unpredictable")
    elif instr[5:12] == "0b1111111" and instr[24:28] == "0b1111":
        raise UndefinedInstructionException()
