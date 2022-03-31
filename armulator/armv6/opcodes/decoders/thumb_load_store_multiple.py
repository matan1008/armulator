from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.concrete.ldm_thumb_t2 import LdmThumbT2
from armulator.armv6.opcodes.concrete.ldmdb_t1 import LdmdbT1
from armulator.armv6.opcodes.concrete.pop_thumb_t2 import PopThumbT2
from armulator.armv6.opcodes.concrete.push_t2 import PushT2
from armulator.armv6.opcodes.concrete.rfe_t1 import RfeT1
from armulator.armv6.opcodes.concrete.rfe_t2 import RfeT2
from armulator.armv6.opcodes.concrete.srs_thumb_t1 import SrsThumbT1
from armulator.armv6.opcodes.concrete.srs_thumb_t2 import SrsThumbT2
from armulator.armv6.opcodes.concrete.stm_t2 import StmT2
from armulator.armv6.opcodes.concrete.stmdb_t1 import StmdbT1


def decode_instruction(instr):
    instr_l = bit_at(instr, 20)
    instr_op = substring(instr, 24, 23)
    instr_w_rn = chain(bit_at(instr, 21), substring(instr, 19, 16), 4)
    if instr_op == 0b00 and not instr_l:
        # Store Return State
        return SrsThumbT1
    elif instr_op == 0b00 and instr_l:
        # Return From Exception
        return RfeT1
    elif instr_op == 0b01 and not instr_l:
        # Store Multiple (Increment After, Empty Ascending)
        return StmT2
    elif instr_op == 0b01 and instr_l and instr_w_rn != 0b11101:
        # Load Multiple (Increment After, Full Descending)
        return LdmThumbT2
    elif instr_op == 0b01 and instr_l and instr_w_rn == 0b11101:
        # Pop Multiple Registers from the stack
        return PopThumbT2
    elif instr_op == 0b10 and not instr_l and instr_w_rn != 0b11101:
        # Store Multiple (Decrement Before, Full Descending)
        return StmdbT1
    elif instr_op == 0b10 and not instr_l and instr_w_rn == 0b11101:
        # Push Multiple Registers to the stack.
        return PushT2
    elif instr_op == 0b10 and instr_l:
        # Load Multiple (Decrement Before, Empty Ascending)
        return LdmdbT1
    elif instr_op == 0b11 and not instr_l:
        # Store Return State
        return SrsThumbT2
    elif instr_op == 0b11 and instr_l:
        # Return From Exception
        return RfeT2
