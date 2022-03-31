from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.rrx import Rrx


class RrxT1(Rrx):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        setflags = bit_at(instr, 20)
        if rd in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return RrxT1(instr, setflags=setflags, m=rm, d=rd)
