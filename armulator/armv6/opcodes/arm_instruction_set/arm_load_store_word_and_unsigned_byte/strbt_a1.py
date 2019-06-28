from armulator.armv6.opcodes.abstract_opcodes.strbt import Strbt
from armulator.armv6.opcodes.opcode import Opcode


class StrbtA1(Strbt, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Strbt.__init__(self, add, False, post_index, t, n, imm32=imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        post_index = True
        imm32 = "0b00000000000000000000" + imm12
        if rt.uint == 15 or rn.uint == 15 or rn.uint == rt.uint:
            print("unpredictable")
        else:
            return StrbtA1(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                     "n": rn.uint, "imm32": imm32})
