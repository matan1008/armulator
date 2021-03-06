from armulator.armv6.opcodes.abstract_opcodes.strb_immediate_thumb import StrbImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class StrbImmediateThumbT2(StrbImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        StrbImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

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
        if rn == "0b1111":
            raise UndefinedInstructionException()
        elif rt.uint in (13, 15):
            print "unpredictable"
        else:
            return StrbImmediateThumbT2(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint,
                                                  "n": rn.uint, "imm32": imm32})
