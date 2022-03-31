from armulator.armv6.opcodes.abstract_opcodes.isb import Isb


class IsbA1(Isb):
    @staticmethod
    def from_bitarray(instr, processor):
        return IsbA1(instr)
