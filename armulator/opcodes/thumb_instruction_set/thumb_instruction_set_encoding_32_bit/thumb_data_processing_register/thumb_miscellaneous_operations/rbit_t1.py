from armulator.opcodes.abstract_opcodes.rbit import Rbit
from armulator.opcodes.opcode import Opcode


class RbitT1(Rbit, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rbit.__init__(self, m, d)

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
            return RbitT1(instr, **{"m": rm.uint, "d": rd.uint})
