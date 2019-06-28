from armulator.armv6.opcodes.abstract_opcodes.ldrb_immediate_thumb import LdrbImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class LdrbImmediateThumbT3(LdrbImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrbImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rn = instr[12:16]
        rt = instr[16:20]
        index = instr[21]
        add = instr[22]
        wback = instr[23]
        imm32 = zero_extend(imm8, 32)
        if not index and not wback:
            raise UndefinedInstructionException()
        elif rt.uint == 13 or (rt.uint == 15 and wback) or (wback and rn.uint == rt.uint):
            print("unpredictable")
        else:
            return LdrbImmediateThumbT3(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint,
                                                  "n": rn.uint, "imm32": imm32})
