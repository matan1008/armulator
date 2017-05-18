from armulator.opcodes.abstract_opcodes.ldc_literal import LdcLiteral
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend
from armulator.arm_exceptions import UndefinedInstructionException


class LdcLiteralT1(LdcLiteral, Opcode):
    def __init__(self, instruction, cp, add, imm32, index):
        Opcode.__init__(self, instruction)
        LdcLiteral.__init__(self, cp, add, imm32, index)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        coproc = instr[20:24]
        add = instr[8]
        index = instr[7]
        imm32 = zero_extend(imm8 + "0b00", 32)
        if instr[7:11] == "0b0000":
            raise UndefinedInstructionException()
        elif instr[10] or not index:
            print "unpredictable"
        else:
            return LdcLiteralT1(instr, **{"cp": coproc.uint, "add": add, "imm32": imm32, "index": index})
