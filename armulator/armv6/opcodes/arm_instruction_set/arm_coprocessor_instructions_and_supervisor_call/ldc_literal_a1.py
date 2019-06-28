from armulator.armv6.opcodes.abstract_opcodes.ldc_literal import LdcLiteral
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import zero_extend


class LdcLiteralA1(LdcLiteral, Opcode):
    def __init__(self, instruction, cp, add, imm32, index):
        Opcode.__init__(self, instruction)
        LdcLiteral.__init__(self, cp, add, imm32, index)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        coproc = instr[20:24]
        w = instr[10]
        add = instr[8]
        index = instr[7]
        d = instr[9]
        if not index and not add and not d and not w:
            raise UndefinedInstructionException()
        elif w:
            print("unpredictable")
        else:
            imm32 = zero_extend(imm8 + "0b00", 32)
            return LdcLiteralA1(instr, **{"cp": coproc.uint, "add": add, "imm32": imm32, "index": index})
