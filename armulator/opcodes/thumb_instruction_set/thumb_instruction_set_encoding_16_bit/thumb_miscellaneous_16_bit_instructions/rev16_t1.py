from armulator.opcodes.abstract_opcodes.rev16 import Rev16
from armulator.opcodes.opcode import Opcode


class Rev16T1(Rev16, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rev16.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rm = instr[10:13]
        return Rev16T1(instr, **{"m": rm.uint, "d": rd.uint})
