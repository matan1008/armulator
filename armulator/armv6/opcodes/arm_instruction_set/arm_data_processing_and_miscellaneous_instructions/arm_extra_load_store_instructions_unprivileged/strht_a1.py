from armulator.armv6.opcodes.abstract_opcodes.strht import Strht
from armulator.armv6.opcodes.opcode import Opcode


class StrhtA1(Strht, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Strht.__init__(self, add, False, post_index, t, n, imm32=imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm4_l = instr[-4:]
        imm4_h = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        post_index = True
        imm32 = "0b000000000000000000000000" + imm4_h + imm4_l
        if rt.uint == 15 or rn.uint == 15 or rt.uint == rn.uint:
            print "unpredictable"
        else:
            return StrhtA1(instr, **{"add": add, "post_index": post_index,
                                     "t": rt.uint, "n": rn.uint, "imm32": imm32})
