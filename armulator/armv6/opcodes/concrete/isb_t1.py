from armulator.armv6.opcodes.abstract_opcodes.isb import Isb


class IsbT1(Isb):
    @staticmethod
    def from_bitarray(instr, processor):
        return IsbT1(instr)
