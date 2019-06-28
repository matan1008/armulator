from armulator.armv6.opcodes.abstract_opcodes.rbit import Rbit
from armulator.armv6.opcodes.opcode import Opcode


class RbitA1(Rbit, Opcode):
    def __init__(self, instruction, m, d):
        Opcode.__init__(self, instruction)
        Rbit.__init__(self, m, d)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[16:20]
        if rm.uint == 15 or rd.uint == 15:
            print("unpredictable")
        else:
            return RbitA1(instr, **{"m": rm.uint, "d": rd.uint})
