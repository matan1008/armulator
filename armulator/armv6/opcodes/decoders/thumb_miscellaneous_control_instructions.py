from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.clrex_t1 import ClrexT1
from armulator.armv6.opcodes.concrete.dsb_t1 import DsbT1
from armulator.armv6.opcodes.concrete.enterx_leavex_t1 import EnterxLeavexT1
from armulator.armv6.opcodes.concrete.isb_t1 import IsbT1


def decode_instruction(instr):
    instr_op = substring(instr, 7, 4)
    if instr_op == 0b0000 or instr_op == 0b0001:
        # Exit ThumbEE state / Enter ThumbEE state
        return EnterxLeavexT1
    elif instr_op == 0b0010:
        # Clear-Exclusive
        return ClrexT1
    elif instr_op == 0b0100:
        # Data Synchronization Barrier
        return DsbT1
    elif instr_op == 0b0101:
        # Data Memory Barrier
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr_op == 0b0110:
        # Instruction Synchronization Barrier
        return IsbT1
