from armulator.opcodes.abstract_opcodes.wfe import Wfe
from armulator.opcodes.opcode import Opcode


class WfeT2(Wfe, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Wfe.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return WfeT2(instr)
