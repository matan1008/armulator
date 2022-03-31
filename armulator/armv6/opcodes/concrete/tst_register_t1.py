from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.tst_register import TstRegister
from armulator.armv6.shift import SRType


class TstRegisterT1(TstRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        shift_t = SRType.LSL
        shift_n = 0
        return TstRegisterT1(instr, m=rm, n=rn, shift_t=shift_t, shift_n=shift_n)
