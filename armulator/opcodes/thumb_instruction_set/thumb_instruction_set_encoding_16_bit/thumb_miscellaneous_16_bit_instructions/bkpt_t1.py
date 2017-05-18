from armulator.opcodes.abstract_opcodes.bkpt import Bkpt
from armulator.opcodes.opcode import Opcode


class BkptT1(Bkpt, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Bkpt.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return BkptT1(instr)
