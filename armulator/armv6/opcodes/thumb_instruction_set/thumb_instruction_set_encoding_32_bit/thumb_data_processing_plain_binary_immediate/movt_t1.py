from armulator.armv6.opcodes.abstract_opcodes.movt import Movt
from armulator.armv6.opcodes.opcode import Opcode


class MovtT1(Movt, Opcode):
    def __init__(self, instruction, d, imm16):
        Opcode.__init__(self, instruction)
        Movt.__init__(self, d, imm16)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        imm4 = instr[12:16]
        i = instr[5:6]
        imm16 = imm4 + i + imm3 + imm8
        if rd.uint in (13, 15):
            print "unpredictable"
        else:
            return MovtT1(instr, **{"d": rd.uint, "imm16": imm16})
