from armulator.opcodes.abstract_opcodes.blx_register import BlxRegister
from armulator.opcodes.opcode import Opcode


class BlxRegisterA1(BlxRegister, Opcode):
    def __init__(self, instruction, m):
        Opcode.__init__(self, instruction)
        BlxRegister.__init__(self, m)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        if rm.uint == 15:
            print "unpredictable"
        else:
            return BlxRegisterA1(instr, **{"m": rm.uint})
