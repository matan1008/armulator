from armulator.armv6.opcodes.abstract_opcodes.eret import Eret


class EretT1(Eret):
    @staticmethod
    def from_bitarray(instr, processor):
        return EretT1(instr)
