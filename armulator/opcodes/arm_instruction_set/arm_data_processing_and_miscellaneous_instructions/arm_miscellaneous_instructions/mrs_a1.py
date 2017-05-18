from armulator.opcodes.abstract_opcodes.mrs import Mrs
from armulator.opcodes.opcode import Opcode


class MrsA1(Mrs, Opcode):
    def __init__(self, instruction, read_spsr, d):
        Opcode.__init__(self, instruction)
        Mrs.__init__(self, read_spsr, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[16:20]
        read_spsr = instr[9]
        if rd.uint == 15:
            print "unpredictable"
        else:
            return MrsA1(instr, **{"read_spsr": read_spsr, "d": rd.uint})
