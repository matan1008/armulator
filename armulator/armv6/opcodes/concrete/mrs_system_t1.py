from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.mrs_system import MrsSystem


class MrsSystemT1(MrsSystem):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 11, 8)
        read_spsr = bit_at(instr, 20)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return MrsSystemT1(instr, read_spsr=read_spsr, d=rd)
