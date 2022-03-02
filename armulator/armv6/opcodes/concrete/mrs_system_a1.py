from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.mrs_system import MrsSystem


class MrsSystemA1(MrsSystem):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 15, 12)
        read_spsr = bit_at(instr, 22)
        if rd == 15:
            print('unpredictable')
        else:
            return MrsSystemA1(instr, read_spsr=read_spsr, d=rd)
