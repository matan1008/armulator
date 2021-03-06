from armulator.armv6.opcodes.abstract_opcodes.stm_user_registers import StmUserRegisters
from armulator.armv6.opcodes.opcode import Opcode


class StmUserRegistersA1(StmUserRegisters, Opcode):
    def __init__(self, instruction, increment, word_higher, registers, n):
        Opcode.__init__(self, instruction)
        StmUserRegisters.__init__(self, increment, word_higher, registers, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        rn = instr[12:16]
        increment = instr[8]
        word_higher = increment == instr[7]
        if rn.uint == 15 or register_list.count(1) < 1:
            print "unpredictable"
        else:
            return StmUserRegistersA1(instr, **{"increment": increment, "word_higher": word_higher,
                                                "registers": register_list, "n": rn.uint})
