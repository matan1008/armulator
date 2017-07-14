from armulator.armv6.opcodes.abstract_opcodes.tbb import Tbb
from armulator.armv6.opcodes.opcode import Opcode


class TbbT1(Tbb, Opcode):
    def __init__(self, instruction, is_tbh, m, n):
        Opcode.__init__(self, instruction)
        Tbb.__init__(self, is_tbh, m, n)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        is_tbh = instr[27]
        rn = instr[12:16]
        if rn.uint == 13 or rm.uint in (13, 15) or (processor.in_it_block() and not processor.last_in_it_block()):
            print "unpredictable"
        else:
            return TbbT1(instr, **{"is_tbh": is_tbh, "m": rm.uint, "n": rn.uint})
