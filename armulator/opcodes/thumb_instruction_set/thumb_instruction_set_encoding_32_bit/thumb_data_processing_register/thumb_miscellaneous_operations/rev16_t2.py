from armulator.opcodes.abstract_opcodes.rev16 import Rev16
from armulator.opcodes.opcode import Opcode


class Rev16T2(Rev16, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rev16.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        rm1 = instr[12:16]
        if rm.uint in (13, 15) or rd.uint in (13, 15) or rm != rm1:
            print "unpredictable"
        else:
            return Rev16T2(instr, **{"m": rm.uint, "d": rd.uint})
