from armulator.armv6.opcodes.abstract_opcodes.setend import Setend
from armulator.armv6.opcodes.opcode import Opcode


class SetendA1(Setend, Opcode):
    def __init__(self, instruction, set_bigend):
        Opcode.__init__(self, instruction)
        Setend.__init__(self, set_bigend)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        set_bigend = instr[22]
        return SetendA1(instr, **{"set_bigend": set_bigend})
