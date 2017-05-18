from armulator.opcodes.abstract_opcodes.rev import Rev
from armulator.opcodes.opcode import Opcode


class RevT1(Rev, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rev.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rm = instr[10:13]
        return RevT1(instr, **{"m": rm.uint, "d": rd.uint})
