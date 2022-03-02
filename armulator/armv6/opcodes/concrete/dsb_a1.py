from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.dsb import Dsb


class DsbA1(Dsb):
    @staticmethod
    def from_bitarray(instr, processor):
        option = substring(instr, 3, 0)
        return DsbA1(instr, option=option)
