from armulator.opcodes.abstract_opcodes.bxj import Bxj
from armulator.opcodes.opcode import Opcode


class BxjA1(Bxj, Opcode):
    def __init__(self, instruction, m):
        Opcode.__init__(self, instruction)
        Bxj.__init__(self, m)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        if rm.uint == 15:
            print "unpredictable"
        else:
            return BxjA1(instr, **{"m": rm.uint})
