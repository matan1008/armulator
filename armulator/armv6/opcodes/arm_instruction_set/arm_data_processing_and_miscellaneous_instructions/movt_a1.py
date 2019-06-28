from armulator.armv6.opcodes.abstract_opcodes.movt import Movt
from armulator.armv6.opcodes.opcode import Opcode


class MovtA1(Movt, Opcode):
    def __init__(self, instruction, d, imm16):
        Opcode.__init__(self, instruction)
        Movt.__init__(self, d, imm16)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rd = instr[16:20]
        imm4 = instr[12:16]
        imm16 = imm4 + imm12
        if rd.uint == 15:
            print("unpredictable")
        else:
            return MovtA1(instr, **{"d": rd.uint, "imm16": imm16})
