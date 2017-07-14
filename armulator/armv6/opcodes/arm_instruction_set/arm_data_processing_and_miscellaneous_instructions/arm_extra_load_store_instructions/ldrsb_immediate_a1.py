from armulator.armv6.opcodes.abstract_opcodes.ldrsb_immediate import LdrsbImmediate
from armulator.armv6.opcodes.opcode import Opcode


class LdrsbImmediateA1(LdrsbImmediate, Opcode):
    def __init__(self, instruction, add, wback, index, imm32, t, n):
        Opcode.__init__(self, instruction)
        LdrsbImmediate.__init__(self, add, wback, index, imm32, t, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        w = instr[10]
        index = instr[7]
        imm4_l = instr[-4:]
        imm4_h = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        imm32 = "0b000000000000000000000000" + imm4_h + imm4_l
        wback = (not index) or w
        if rt.uint == 15 or (wback and rn.uint == rt.uint):
            print "unpredictable"
        else:
            return LdrsbImmediateA1(instr, **{"add": add, "wback": wback, "index": index, "imm32": imm32,
                                              "t": rt.uint, "n": rn.uint})
