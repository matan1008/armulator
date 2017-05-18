from armulator.opcodes.abstract_opcodes.ldrt import Ldrt
from armulator.opcodes.opcode import Opcode


class LdrtA1(Ldrt, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Ldrt.__init__(self, add, False, post_index, t, n, imm32=imm32)

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
            return LdrtA1(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                    "n": rn.uint, "imm32": imm32})
