from armulator.armv6.opcodes.abstract_opcodes.setend import Setend
from armulator.armv6.opcodes.opcode import Opcode


class SetendT1(Setend, Opcode):
    def __init__(self, instruction, set_bigend):
        Opcode.__init__(self, instruction)
        Setend.__init__(self, set_bigend)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        set_bigend = instr[12]
        if processor.in_it_block():
            print("unpredictable")
        else:
            return SetendT1(instr, **{"set_bigend": set_bigend})
