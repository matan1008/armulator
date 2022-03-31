from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.smc import Smc


class SmcA1(Smc):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 3, 0)
        return SmcA1(instr)
