from armulator.opcodes.abstract_opcodes.ldrsb_immediate import LdrsbImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend
from armulator.arm_exceptions import UndefinedInstructionException


class LdrsbImmediateT2(LdrsbImmediate, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrsbImmediate.__init__(self, add, wback, index, imm32, t, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rn = instr[12:16]
        rt = instr[16:20]
        index = instr[21]
        add = instr[22]
        wback = instr[23]
        imm32 = zero_extend(imm8, 32)
        if not index and not wback:
            raise UndefinedInstructionException()
        elif rt.uint == 13 or (rt.uint == 15 and wback) or (wback and rn.uint == rt.uint):
            print "unpredictable"
        else:
            return LdrsbImmediateT2(instr, **{"add": add, "wback": wback, "index": index, "imm32": imm32, "t": rt.uint,
                                              "n": rn.uint})
