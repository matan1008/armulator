from mrs_a1 import MrsA1
from msr_register_application_a1 import MsrRegisterApplicationA1
from msr_register_system_a1 import MsrRegisterSystemA1
from bx_a1 import BxA1
from clz_a1 import ClzA1
from bxj_a1 import BxjA1
from blx_register_a1 import BlxRegisterA1
import arm_saturating_addition_and_subtraction
from bkpt_a1 import BkptA1
from smc_a1 import SmcA1


def decode_instruction(instr):
    if instr[25:28] == "0b000" and instr[22] and not instr[10]:
        # Move from Banked or Special register, ARMv7VE Only
        raise NotImplementedError()
    elif instr[25:28] == "0b000" and instr[22] and instr[10]:
        # Move to Banked or Special register, ARMv7VE Only
        raise NotImplementedError()
    elif instr[25:28] == "0b000" and not instr[22] and not instr[10]:
        # Move from Special register
        return MrsA1
    elif instr[25:28] == "0b000" and not instr[22] and instr[9:11] == "0b01" and instr[14:16] == "0b00":
        # Move to Special register, Application level
        return MsrRegisterApplicationA1
    elif instr[25:28] == "0b000" and not instr[22] and instr[9:11] == "0b01" and (instr[14:16] == "0b01" or instr[14]):
        # Move to Special register, System level
        return MsrRegisterSystemA1
    elif instr[25:28] == "0b000" and not instr[22] and instr[9:11] == "0b11":
        # Move to Special register, System level
        return MsrRegisterSystemA1
    elif instr[25:28] == "0b001" and instr[9:11] == "0b01":
        # Branch and Exchange
        return BxA1
    elif instr[25:28] == "0b001" and instr[9:11] == "0b11":
        # Count Leading Zeros
        return ClzA1
    elif instr[25:28] == "0b010" and instr[9:11] == "0b01":
        # Branch and Exchange Jazelle
        return BxjA1
    elif instr[25:28] == "0b011" and instr[9:11] == "0b01":
        # Branch with Link and Exchange
        return BlxRegisterA1
    elif instr[25:28] == "0b101":
        return arm_saturating_addition_and_subtraction.decode_instruction(instr)
    elif instr[25:28] == "0b110" and instr[9:11] == "0b11":
        # Exception Return, ARMv7VE
        raise NotImplementedError()
    elif instr[25:28] == "0b111" and instr[9:11] == "0b01":
        # Breakpoint
        return BkptA1
    elif instr[25:28] == "0b111" and instr[9:11] == "0b10":
        # Hypervisor Call, ARMv7VE
        raise NotImplementedError()
    elif instr[25:28] == "0b111" and instr[9:11] == "0b11":
        # Secure Monitor Call
        return SmcA1
