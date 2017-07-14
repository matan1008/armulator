from armulator.armv6.opcodes.abstract_opcodes.blx_register import BlxRegister
from armulator.armv6.opcodes.opcode import Opcode


class BlxRegisterT1(BlxRegister, Opcode):
    def __init__(self, instruction, m):
        Opcode.__init__(self, instruction)
        BlxRegister.__init__(self, m)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[9:13]
        if rm.uint == 15 or (processor.in_it_block() and not processor.last_in_it_block()):
            print "unpredictable"
        else:
            return BlxRegisterT1(instr, **{"m": rm.uint})
