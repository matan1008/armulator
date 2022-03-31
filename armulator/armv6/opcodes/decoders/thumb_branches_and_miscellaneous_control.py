from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.concrete.b_t3 import BT3
from armulator.armv6.opcodes.concrete.b_t4 import BT4
from armulator.armv6.opcodes.concrete.bl_blx_immediate_t1 import BlBlxImmediateT1
from armulator.armv6.opcodes.concrete.bl_blx_immediate_t2 import BlBlxImmediateT2
from armulator.armv6.opcodes.concrete.bxj_t1 import BxjT1
from armulator.armv6.opcodes.concrete.eret_t1 import EretT1
from armulator.armv6.opcodes.concrete.mrs_application_t1 import MrsApplicationT1
from armulator.armv6.opcodes.concrete.mrs_system_t1 import MrsSystemT1
from armulator.armv6.opcodes.concrete.msr_register_application_t1 import MsrRegisterApplicationT1
from armulator.armv6.opcodes.concrete.msr_register_system_t1 import MsrRegisterSystemT1
from armulator.armv6.opcodes.concrete.smc_t1 import SmcT1
from armulator.armv6.opcodes.concrete.subs_pc_lr_thumb_t1 import SubsPcLrThumbT1
from armulator.armv6.opcodes.concrete.udf_t2 import UdfT2
from armulator.armv6.opcodes.decoders import thumb_change_processor_state_and_hints
from armulator.armv6.opcodes.decoders import thumb_miscellaneous_control_instructions


def decode_instruction(instr):
    instr_14 = bit_at(instr, 14)
    instr_12 = bit_at(instr, 12)
    instr_5 = bit_at(instr, 5)
    instr_op = substring(instr, 26, 20)
    instr_9_8 = substring(instr, 9, 8)
    instr_14_12 = substring(instr, 14, 12)
    if not instr_14 and not instr_12 and substring(instr, 25, 23) != 0b111:
        # Conditional branch
        return BT3
    elif not instr_14 and not instr_12 and instr_5 and substring(instr, 26, 21) == 0b011100:
        # Move to Banked or Special register
        # armv7, will not be implemented
        raise NotImplementedError()
    elif not instr_14 and not instr_12 and not instr_5 and instr_op == 0b0111000 and instr_9_8 == 0b00:
        # Move to Special register, Application level
        return MsrRegisterApplicationT1
    elif not instr_14 and not instr_12 and not instr_5 and (
            (instr_op == 0b0111000 and (instr_9_8 == 0b01 or bit_at(instr, 9))) or instr_op == 0b0111001):
        # Move to Special register, System level
        return MsrRegisterSystemT1
    elif not instr_14 and not instr_12 and instr_op == 0b0111010:
        # Change Processor State, and hints
        return thumb_change_processor_state_and_hints.decode_instruction(instr)
    elif not instr_14 and not instr_12 and instr_op == 0b0111011:
        # Miscellaneous control instructions
        return thumb_miscellaneous_control_instructions.decode_instruction(instr)
    elif not instr_14 and not instr_12 and instr_op == 0b0111100:
        # Branch and Exchange Jazelle
        return BxjT1
    elif not instr_14 and not instr_12 and substring(instr, 7, 0) == 0b00000000 and instr_op == 0b0111101:
        # Exception Return
        return EretT1
    elif not instr_14 and not instr_12 and substring(instr, 7, 0) != 0b00000000 and instr_op == 0b0111101:
        # Exception Return
        return SubsPcLrThumbT1
    elif not instr_14 and not instr_12 and instr_5 and instr[5:11] == 0b011111:
        # Move from Banked or Special register
        # armv7, will not be implemented
        raise NotImplementedError()
    elif not instr_14 and not instr_12 and not instr_5 and instr_op == 0b0111110:
        # Move from Special register, Application level
        return MrsApplicationT1
    elif not instr_14 and not instr_12 and not instr_5 and instr_op == 0b0111111:
        # Move from Special register, System level
        return MrsSystemT1
    elif instr_14_12 == 0b000 and instr_op == 0b1111110:
        # Hypervisor Call
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr_14_12 == 0b000 and instr_op == 0b1111111:
        # Secure Monitor Call
        return SmcT1
    elif not instr_14 and instr_12:
        # Branch
        return BT4
    elif instr_14_12 == 0b010 and instr_op == 0b1111111:
        # Permanently UNDEFINED
        return UdfT2
    elif instr_14 and not instr_12:
        # Branch with Link and Exchange
        return BlBlxImmediateT2
    elif instr_14 and instr_12:
        # Branch with Link
        return BlBlxImmediateT1
