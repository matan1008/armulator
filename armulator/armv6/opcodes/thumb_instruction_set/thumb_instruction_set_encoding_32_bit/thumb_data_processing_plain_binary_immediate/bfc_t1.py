from armulator.armv6.opcodes.abstract_opcodes.bfc import Bfc
from armulator.armv6.opcodes.opcode import Opcode


class BfcT1(Bfc, Opcode):
    def __init__(self, instruction, lsbit, msbit, d):
        Opcode.__init__(self, instruction)
        Bfc.__init__(self, lsbit, msbit, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        msb = instr[27:32]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        lsbit = (imm3 + imm2).uint
        if rd.uint in (13, 15):
            print("unpredictable")
        else:
            return BfcT1(instr, **{"lsbit": lsbit, "msbit": msb.uint, "d": rd.uint})
