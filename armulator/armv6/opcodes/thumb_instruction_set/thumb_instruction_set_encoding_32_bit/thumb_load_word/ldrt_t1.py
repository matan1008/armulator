from armulator.armv6.opcodes.abstract_opcodes.ldrt import Ldrt
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrtT1(Ldrt, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Ldrt.__init__(self, add, False, post_index, t, n, imm32=imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rt = instr[16:20]
        rn = instr[12:16]
        post_index = False
        add = True
        imm32 = zero_extend(imm8, 32)
        if rt.uint in (13, 15):
            print("unpredictable")
        else:
            return LdrtT1(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                    "n": rn.uint, "imm32": imm32})
