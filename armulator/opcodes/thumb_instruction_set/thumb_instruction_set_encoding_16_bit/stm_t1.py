from armulator.opcodes.abstract_opcodes.stm import Stm
from armulator.opcodes.opcode import Opcode


class StmT1(Stm, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        Stm.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[8:16]
        rn = instr[5:8]
        wback = True
        registers = "0b00000000" + register_list
        if registers.count(1) < 1:
            print "unpredictable"
        else:
            return StmT1(instr, **{"wback": wback, "registers": registers, "n": rn.uint})
