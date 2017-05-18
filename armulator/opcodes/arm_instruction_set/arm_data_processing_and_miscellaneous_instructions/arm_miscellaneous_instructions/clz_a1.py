from armulator.opcodes.abstract_opcodes.clz import Clz
from armulator.opcodes.opcode import Opcode


class ClzA1(Clz, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Clz.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        rd = instr[16:20]
        if rm.uint == 15 or rd.uint == 15:
            print "unpredictable"
        else:
            return ClzA1(instr, **{"m": rm.uint, "d": rd.uint})
