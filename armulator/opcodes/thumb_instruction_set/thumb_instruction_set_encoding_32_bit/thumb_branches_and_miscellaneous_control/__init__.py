from b_t3 import BT3
from msr_register_application_t1 import MsrRegisterApplicationT1
from msr_register_system_t1 import MsrRegisterSystemT1
import thumb_change_processor_state_and_hints
import thumb_miscellaneous_control_instructions
from bxj_t1 import BxjT1
from eret_t1 import EretT1
from subs_pc_lr_thumb_t1 import SubsPcLrThumbT1
from mrs_application_t1 import MrsApplicationT1
from mrs_t1 import MrsT1
from smc_t1 import SmcT1
from b_t4 import BT4
from udf_t2 import UdfT2
from bl_immediate_t2 import BlImmediateT2
from bl_immediate_t1 import BlImmediateT1


def decode_instruction(instr):
    if not instr[17] and not instr[19] and instr[6:9] != "111":
        # Conditional branch
        return BT3
    elif not instr[17] and not instr[19] and instr[26] and instr[5:11] == "0b011100":
        # Move to Banked or Special register
        # armv7, will not be implemented
        raise NotImplementedError()
    elif not instr[17] and not instr[19] and not instr[26] and instr[5:12] == "0b0111000" and instr[22:24] == "0b00":
        # Move to Special register, Application level
        return MsrRegisterApplicationT1
    elif not instr[17] and not instr[19] and not instr[26] and (
                (instr[5:12] == "0b0111000" and (instr[22:24] == "0b01" or instr[22])) or instr[5:12] == "0b0111001"):
        # Move to Special register, System level
        return MsrRegisterSystemT1
    elif not instr[17] and not instr[19] and instr[5:12] == "0b0111010":
        # Change Processor State, and hints
        return thumb_change_processor_state_and_hints.decode_instruction(instr)
    elif not instr[17] and not instr[19] and instr[5:12] == "0b0111011":
        # Miscellaneous control instructions
        return thumb_miscellaneous_control_instructions.decode_instruction(instr)
    elif not instr[17] and not instr[19] and instr[5:12] == "0b0111100":
        # Branch and Exchange Jazelle
        return BxjT1
    elif not instr[17] and not instr[19] and instr[24:32] == "0b00000000" and instr[5:12] == "0b0111101":
        # Exception Return
        return EretT1
    elif not instr[17] and not instr[19] and instr[24:32] != "0b00000000" and instr[5:12] == "0b0111101":
        # Exception Return
        return SubsPcLrThumbT1
    elif not instr[17] and not instr[19] and instr[26] and instr[5:11] == "0b011111":
        # Move from Banked or Special register
        # armv7, will not be implemented
        raise NotImplementedError()
    elif not instr[17] and not instr[19] and not instr[26] and instr[5:12] == "0b0111110":
        # Move from Special register, Application level
        return MrsApplicationT1
    elif not instr[17] and not instr[19] and not instr[26] and instr[5:12] == "0b0111111":
        # Move from Special register, System level
        return MrsT1
    elif instr[17:20] == "0b000" and instr[5:12] == "0b1111110":
        # Hypervisor Call
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr[17:20] == "0b000" and instr[5:12] == "0b1111111":
        # Secure Monitor Call
        return SmcT1
    elif not instr[17] and instr[19]:
        # Branch
        return BT4
    elif instr[17:20] == "0b010" and instr[5:12] == "0b1111111":
        # Permanently UNDEFINED
        return UdfT2
    elif instr[17] and not instr[19]:
        # Branch with Link and Exchange
        return BlImmediateT2
    elif instr[17] and instr[19]:
        # Branch with Link
        return BlImmediateT1
