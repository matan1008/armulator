from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.strh_register import StrhRegister
from armulator.armv6.shift import SRType


class StrhRegisterA1(StrhRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        w = bit_at(instr, 21)
        p = bit_at(instr, 24)
        rm = substring(instr, 3, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        wback = (not p) or w
        shift_t = SRType.LSL
        shift_n = 0
        if rt == 15 or rm == 15 or (wback and (rn == 15 or rn == rt)) or (arch_version() < 6 and wback and rm == rn):
            print('unpredictable')
        else:
            return StrhRegisterA1(instr, add=add, wback=wback, index=p, m=rm, t=rt, n=rn, shift_t=shift_t,
                                  shift_n=shift_n)
