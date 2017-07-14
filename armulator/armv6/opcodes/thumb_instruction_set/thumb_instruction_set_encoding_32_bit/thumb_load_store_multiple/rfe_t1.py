from armulator.armv6.opcodes.abstract_opcodes.rfe import Rfe
from armulator.armv6.opcodes.opcode import Opcode


class RfeT1(Rfe, Opcode):
    def __init__(self, instruction, word_higher, wback, n):
        Opcode.__init__(self, instruction)
        Rfe.__init__(self, False, word_higher, wback, n)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[12:16]
        wback = instr[10]
        wordhigher = False
        if rn.uint == 15 or (processor.in_it_block() and not processor.last_in_it_block()):
            print "unpredictable"
        else:
            return RfeT1(instr, **{"word_higher": wordhigher, "wback": wback, "n": rn.uint})
