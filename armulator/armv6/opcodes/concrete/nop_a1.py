from armulator.armv6.opcodes.abstract_opcodes.nop import Nop


class NopA1(Nop):
    @staticmethod
    def from_bitarray(instr, processor):
        return NopA1(instr)
