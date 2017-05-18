from armulator.opcodes.abstract_opcodes.bfc import Bfc
from armulator.opcodes.opcode import Opcode


class BfcA1(Bfc, Opcode):
    def __init__(self, instruction, lsbit, msbit, d):
        Opcode.__init__(self, instruction)
        Bfc.__init__(self, lsbit, msbit, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        lsb = instr[20:25]
        rd = instr[16:20]
        msb = instr[11:16]
        if rd.uint == 15:
            print "unpredictable"
        else:
            return BfcA1(instr, **{"lsbit": lsb.uint, "msbit": msb.uint, "d": rd.uint})
