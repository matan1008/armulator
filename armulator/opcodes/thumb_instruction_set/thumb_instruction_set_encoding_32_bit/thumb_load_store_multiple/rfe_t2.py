from armulator.opcodes.abstract_opcodes.rfe import Rfe
from armulator.opcodes.opcode import Opcode


class RfeT2(Rfe, Opcode):
    def __init__(self, instruction, word_higher, wback, n):
        Opcode.__init__(self, instruction)
        Rfe.__init__(self, True, word_higher, wback, n)

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
            return RfeT2(instr, **{"word_higher": wordhigher, "wback": wback, "n": rn.uint})
