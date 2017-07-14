from armulator.armv6.opcodes.abstract_opcodes.dsb import Dsb
from armulator.armv6.opcodes.opcode import Opcode


class DsbT1(Dsb, Opcode):
    def __init__(self, instruction, option):
        Opcode.__init__(self, instruction)
        Dsb.__init__(self, option)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        option = instr[28:32]
        return DsbT1(instr, **{"option": option})
