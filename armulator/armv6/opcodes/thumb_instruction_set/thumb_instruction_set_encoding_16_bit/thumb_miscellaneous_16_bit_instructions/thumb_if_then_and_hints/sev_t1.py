from armulator.armv6.opcodes.abstract_opcodes.sev import Sev
from armulator.armv6.opcodes.opcode import Opcode


class SevT1(Sev, Opcode):
    def __init__(self, instruction):
        Opcode.__init__(self, instruction)
        Sev.__init__(self)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        return SevT1(instr)
