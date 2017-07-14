from armulator.armv6.opcodes.abstract_opcodes.revsh import Revsh
from armulator.armv6.opcodes.opcode import Opcode


class RevshT2(Revsh, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Revsh.__init__(self, m, d)

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
            return RevshT2(instr, **{"m": rm.uint, "d": rd.uint})
