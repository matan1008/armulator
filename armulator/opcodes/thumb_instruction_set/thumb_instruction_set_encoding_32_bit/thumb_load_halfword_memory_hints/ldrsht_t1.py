from armulator.opcodes.abstract_opcodes.ldrsht import Ldrsht
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class LdrshtT1(Ldrsht, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Ldrsht.__init__(self, add, False, post_index, t, n, imm32=imm32)

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
            print "unpredictable"
        else:
            return LdrshtT1(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                      "n": rn.uint, "imm32": imm32})
