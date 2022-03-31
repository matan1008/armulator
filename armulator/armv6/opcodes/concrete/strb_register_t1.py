from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strb_register import StrbRegister
from armulator.armv6.shift import SRType


class StrbRegisterT1(StrbRegister):
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
        return StrbRegisterT1(instr, add=add, wback=wback, index=index, m=rm, t=rt, n=rn, shift_t=shift_t,
                              shift_n=shift_n)
