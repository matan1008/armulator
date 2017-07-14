from armulator.armv6.opcodes.abstract_opcodes.stmib import Stmib
from armulator.armv6.opcodes.opcode import Opcode


class StmibA1(Stmib, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        Stmib.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        rn = instr[12:16]
        wback = instr[10]
        if rn.uint == 15 or register_list.count(1) < 1:
            print "unpredictable"
        else:
            return StmibA1(instr, **{"wback": wback, "registers": register_list, "n": rn.uint})
