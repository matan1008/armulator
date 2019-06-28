from armulator.armv6.opcodes.abstract_opcodes.mrs import Mrs
from armulator.armv6.opcodes.opcode import Opcode


class MrsT1(Mrs, Opcode):
    def __init__(self, instruction, read_spsr, d):
        Opcode.__init__(self, instruction)
        Mrs.__init__(self, read_spsr, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[20:24]
        read_spsr = instr[11]
        if rd.uint in (13, 15):
            print("unpredictable")
        else:
            return MrsT1(instr, **{"read_spsr": read_spsr, "d": rd.uint})
