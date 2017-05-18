from armulator.opcodes.abstract_opcodes.ldrsb_immediate import LdrsbImmediate
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class LdrsbImmediateT1(LdrsbImmediate, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrsbImmediate.__init__(self, add, wback, index, imm32, t, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rt = instr[16:20]
        rn = instr[12:16]
        imm32 = zero_extend(imm12, 32)
        index = True
        add = True
        wback = False
        if rt.uint == 13:
            print "unpredictable"
        else:
            return LdrsbImmediateT1(instr, **{"add": add, "wback": wback, "index": index, "imm32": imm32, "t": rt.uint,
                                              "n": rn.uint})
