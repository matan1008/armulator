from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.cmp_register import CmpRegister
from armulator.armv6.shift import SRType


class CmpRegisterT2(CmpRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = chain(bit_at(instr, 7), substring(instr, 2, 0), 3)
        rm = substring(instr, 6, 3)
        shift_t = SRType.LSL
        shift_n = 0
        if (rn < 8 and rm < 8) or rn == 15 or rm == 15:
            print('unpredictable')
        else:
            return CmpRegisterT2(instr, m=rm, n=rn, shift_t=shift_t, shift_n=shift_n)
