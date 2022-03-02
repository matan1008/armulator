from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.cmp_register import CmpRegister
from armulator.armv6.shift import SRType


class CmpRegisterT1(CmpRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        shift_t = SRType.LSL
        shift_n = 0
        return CmpRegisterT1(instr, m=rm, n=rn, shift_t=shift_t, shift_n=shift_n)
