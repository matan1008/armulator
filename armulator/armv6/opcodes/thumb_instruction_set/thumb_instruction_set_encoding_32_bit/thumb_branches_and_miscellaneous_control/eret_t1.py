from armulator.armv6.opcodes.abstract_opcodes.eret import Eret
from armulator.armv6.opcodes.opcode import Opcode


class EretT1(Eret, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Eret.__init__(self)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        return EretT1(instr)
