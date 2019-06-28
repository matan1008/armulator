from armulator.armv6.opcodes.abstract_opcodes.ldrd_immediate import LdrdImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrdImmediateT1(LdrdImmediate, Opcode):
    def __init__(self, instruction, add, wback, index, imm32, t, t2, n):
        Opcode.__init__(self, instruction)
        LdrdImmediate.__init__(self, add, wback, index, imm32, t, t2, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rt2 = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        index = instr[7]
        add = instr[8]
        wback = instr[10]
        imm32 = zero_extend(imm8 + "0b00", 32)
        if ((wback and (rn.uint == rt.uint or rn.uint == rt2.uint)) or
                rt.uint == rt2.uint or
                rt.uint in (13, 15) or
                rt2.uint in (13, 15)):
            print("unpredictable")
        else:
            return LdrdImmediateT1(instr, **{"add": add, "wback": wback, "index": index, "imm32": imm32, "t": rt.uint,
                                             "t2": rt2.uint, "n": rn.uint})
