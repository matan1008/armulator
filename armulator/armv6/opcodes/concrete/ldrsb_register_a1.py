from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.ldrsb_register import LdrsbRegister
from armulator.armv6.shift import SRType


class LdrsbRegisterA1(LdrsbRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        w = bit_at(instr, 21)
        index = bit_at(instr, 24)
        wback = (not index) or w
        shift_t = SRType.LSL
        shift_n = 0
        if rt == 15 or rm == 15 or (wback and (rn == 15 and rn == rt)) or (arch_version() < 6 and wback and rm == rn):
            print('unpredictable')
        else:
            return LdrsbRegisterA1(instr, add=add, wback=wback, index=index, m=rm, t=rt, n=rn, shift_t=shift_t,
                                   shift_n=shift_n)
