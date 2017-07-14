from armulator.armv6.opcodes.abstract_opcodes.ldrbt import Ldrbt
from armulator.armv6.opcodes.opcode import Opcode


class LdrbtA1(Ldrbt, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Ldrbt.__init__(self, add, False, post_index, t, n, imm32=imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        rn = instr[12:16]
        imm12 = instr[20:32]
        imm32 = "0b00000000000000000000" + imm12
        add = instr[8]
        post_index = True
        if rt.uint == 15 or rn.uint == 15 or rt.uint == rn.uint:
            print "unpredictable"
        else:
            return LdrbtA1(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                     "n": rn.uint, "imm32": imm32})
