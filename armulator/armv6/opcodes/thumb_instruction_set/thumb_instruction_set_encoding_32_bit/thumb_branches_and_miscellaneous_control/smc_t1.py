from armulator.armv6.opcodes.abstract_opcodes.smc import Smc
from armulator.armv6.opcodes.opcode import Opcode


class SmcT1(Smc, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Smc.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        if processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return SmcT1(instr)
