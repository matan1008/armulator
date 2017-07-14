from armulator.armv6.opcodes.abstract_opcodes.enterx import Enterx
from armulator.armv6.opcodes.opcode import Opcode


class EnterxT1(Enterx, Opcode):
    def __init__(self, instruction, is_enterx):
        Opcode.__init__(self, instruction)
        Enterx.__init__(self, is_enterx)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        is_enterx = instr[27]
        return EnterxT1(instr, **{"is_enterx": is_enterx})
