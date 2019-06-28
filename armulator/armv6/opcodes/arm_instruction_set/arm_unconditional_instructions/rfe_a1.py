from armulator.armv6.opcodes.abstract_opcodes.rfe import Rfe
from armulator.armv6.opcodes.opcode import Opcode


class RfeA1(Rfe, Opcode):
    def __init__(self, instruction, increment, word_higher, wback, n):
        Opcode.__init__(self, instruction)
        Rfe.__init__(self, increment, word_higher, wback, n)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        wback = instr[10]
        increment = instr[8]
        p = instr[7]
        word_higher = p == increment
        rn = instr[12:16]
        if rn.uint == 15:
            print("unpredictable")
        else:
            return RfeA1(instr, **{"increment": increment, "word_higher": word_higher, "wback": wback, "n": rn.uint})
