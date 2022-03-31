from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.rev import Rev


class RevT1(Rev):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        return RevT1(instr, m=rm, d=rd)
