from armulator.armv6.opcodes.abstract_opcodes.ldrsh_immediate import LdrshImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrshImmediateT1(LdrshImmediate, Opcode):
    def __init__(self, instruction, add, wback, index, imm32, t, n):
        Opcode.__init__(self, instruction)
        LdrshImmediate.__init__(self, add, wback, index, imm32, t, n)

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
            print("unpredictable")
        else:
            return LdrshImmediateT1(instr, **{"add": add, "wback": wback, "index": index, "imm32": imm32, "t": rt.uint,
                                              "n": rn.uint})
