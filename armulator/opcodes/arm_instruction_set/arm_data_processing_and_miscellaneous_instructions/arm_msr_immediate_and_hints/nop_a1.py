from armulator.opcodes.abstract_opcodes.nop import Nop
from armulator.opcodes.opcode import Opcode


class NopA1(Nop, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Nop.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return NopA1(instr)
