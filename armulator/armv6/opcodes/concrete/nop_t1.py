from armulator.armv6.opcodes.abstract_opcodes.nop import Nop


class NopT1(Nop):
    @staticmethod
    def from_bitarray(instr, processor):
        return NopT1(instr)
