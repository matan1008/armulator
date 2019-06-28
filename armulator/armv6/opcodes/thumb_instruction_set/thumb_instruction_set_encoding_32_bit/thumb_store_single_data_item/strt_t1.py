from armulator.armv6.opcodes.abstract_opcodes.strt import Strt
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import zero_extend


class StrtT1(Strt, Opcode):
    def __init__(self, instruction, add, post_index, t, n, imm32):
        Opcode.__init__(self, instruction)
        Strt.__init__(self, add, False, post_index, t, n, imm32=imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rt = instr[16:20]
        rn = instr[12:16]
        add = True
        post_index = False
        imm32 = zero_extend(imm8, 32)
        if rn == "0b1111":
            raise UndefinedInstructionException()
        elif rt.uint in (13, 15):
            print("unpredictable")
        else:
            return StrtT1(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                    "n": rn.uint, "imm32": imm32})
