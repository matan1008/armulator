from armulator.armv6.opcodes.abstract_opcodes.stmda import Stmda
from armulator.armv6.opcodes.opcode import Opcode


class StmdaA1(Stmda, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        Stmda.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        rn = instr[12:16]
        wback = instr[10]
        if rn.uint == 15 or register_list.count(1) < 1:
            print("unpredictable")
        else:
            return StmdaA1(instr, **{"wback": wback, "registers": register_list, "n": rn.uint})
