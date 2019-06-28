from armulator.armv6.opcodes.abstract_opcodes.rev16 import Rev16
from armulator.armv6.opcodes.opcode import Opcode


class Rev16A1(Rev16, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rev16.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[16:20]
        if rd.uint == 15 or rm.uint == 15:
            print("unpredictable")
        else:
            return Rev16A1(instr, **{"m": rm.uint, "d": rd.uint})
