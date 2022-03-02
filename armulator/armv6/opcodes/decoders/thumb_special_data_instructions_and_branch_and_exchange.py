from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.add_register_thumb_t2 import AddRegisterThumbT2
from armulator.armv6.opcodes.concrete.add_sp_plus_register_thumb_t1 import AddSpPlusRegisterThumbT1
from armulator.armv6.opcodes.concrete.add_sp_plus_register_thumb_t2 import AddSpPlusRegisterThumbT2
from armulator.armv6.opcodes.concrete.cmp_register_t2 import CmpRegisterT2
from armulator.armv6.opcodes.concrete.blx_register_t1 import BlxRegisterT1
from armulator.armv6.opcodes.concrete.bx_t1 import BxT1
from armulator.armv6.opcodes.concrete.mov_register_thumb_t1 import MovRegisterThumbT1


def decode_instruction(instr):
    instr_9_6 = substring(instr, 9, 6)
    instr_9_7 = substring(instr, 9, 7)
    if instr_9_6 == 0b0000 or instr_9_6 == 0b0001 or instr_9_7 == 0b001:
        # Add Low Registers / Add High Registers
        if substring(instr, 6, 3) == 0b1101:
            return AddSpPlusRegisterThumbT1
        elif bit_at(instr, 7) and substring(instr, 2, 0) == 0b101:
            return AddSpPlusRegisterThumbT2
        else:
            return AddRegisterThumbT2
    elif substring(instr, 9, 8) == 0b01:
        # Compare High Registers
        return CmpRegisterT2
    elif instr_9_6 == 0b1000 or instr_9_6 == 0b1001 or instr_9_7 == 0b101:
        # Move Low Registers / Move High Registers
        return MovRegisterThumbT1
    elif instr_9_7 == 0b110:
        # Branch and Exchange
        return BxT1
    elif instr_9_7 == 0b111:
        # Branch with Link and Exchange
        return BlxRegisterT1
