from armulator.armv6.opcodes.abstract_opcodes.stmdb import Stmdb
from armulator.armv6.opcodes.opcode import Opcode


class StmdbT1(Stmdb, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        Stmdb.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[19:32]
        m = instr[17:18]
        wback = instr[10]
        rn = instr[12:16]
        registers = "0b0" + m + "0b0" + register_list
        if rn.uint == 15 or registers.count(1) < 2 or (wback and registers[15 - rn.uint]):
            print("unpredictable")
        else:
            return StmdbT1(instr, **{"wback": wback, "registers": registers, "n": rn.uint})
