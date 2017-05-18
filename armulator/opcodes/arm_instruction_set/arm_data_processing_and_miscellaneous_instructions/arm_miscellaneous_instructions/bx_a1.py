from armulator.opcodes.abstract_opcodes.bx import Bx
from armulator.opcodes.opcode import Opcode


class BxA1(Bx, Opcode):
    def __init__(self, instruction, m):
        Opcode.__init__(self, instruction)
        Bx.__init__(self, m)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        return BxA1(instr, **{"m": rm.uint})
