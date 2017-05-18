from armulator.opcodes.abstract_opcodes.rev import Rev
from armulator.opcodes.opcode import Opcode


class RevA1(Rev, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rev.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[16:20]
        if rd.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return RevA1(instr, **{"m": rm.uint, "d": rd.uint})
