from armulator.armv6.opcodes.abstract_opcodes.ldc_literal import LdcLiteral
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class LdcLiteralA2(LdcLiteral, Opcode):
    def __init__(self, instruction, cp, add, imm32, index):
        Opcode.__init__(self, instruction)
        LdcLiteral.__init__(self, cp, add, imm32, index)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        coproc = instr[20:24]
        index = instr[7]
        add = instr[8]
        wback = instr[10]
        if coproc[0:3] == "0b101":
            raise UndefinedInstructionException()
        elif wback:
            print "unpredictable"
        else:
            imm32 = sign_extend(imm8 + "0b00", 32)
            return LdcLiteralA2(instr, **{"cp": coproc.uint, "add": add, "imm32": imm32, "index": index})
