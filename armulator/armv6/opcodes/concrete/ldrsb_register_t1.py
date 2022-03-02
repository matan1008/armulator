from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrsb_register import LdrsbRegister
from armulator.armv6.shift import SRType


class LdrsbRegisterT1(LdrsbRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        rm = substring(instr, 8, 6)
        index = True
        add = True
        wback = False
        shift_t = SRType.LSL
        shift_n = 0
        return LdrsbRegisterT1(instr, add=add, wback=wback, index=index, m=rm, t=rt, n=rn, shift_t=shift_t,
                               shift_n=shift_n)
