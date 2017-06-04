from armulator.opcodes.abstract_opcodes.ldm_exception_return import LdmExceptionReturn
from armulator.opcodes.opcode import Opcode
from armulator.configurations import arch_version


class LdmExceptionReturnA1(LdmExceptionReturn, Opcode):
    def __init__(self, instruction, increment, word_higher, wback, registers, n):
        Opcode.__init__(self, instruction)
        LdmExceptionReturn.__init__(self, increment, word_higher, wback, registers, n)

    def is_pc_changing_opcode(self):
        return True

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        rn = instr[12:16]
        increment = instr[8]
        word_higher = increment == instr[7]
        wback = instr[10]
        if rn.uint == 15 or (wback and register_list[15 - rn.uint] and arch_version() >= 7):
            print "unpredictable"
        else:
            return LdmExceptionReturnA1(instr, **{"increment": increment, "word_higher": word_higher, "wback": wback,
                                                  "registers": register_list, "n": rn.uint})
