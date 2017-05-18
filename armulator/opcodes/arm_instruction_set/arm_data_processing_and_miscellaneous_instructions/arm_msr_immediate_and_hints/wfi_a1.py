from armulator.opcodes.abstract_opcodes.wfi import Wfi
from armulator.opcodes.opcode import Opcode


class WfiA1(Wfi, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Wfi.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return WfiA1(instr)
