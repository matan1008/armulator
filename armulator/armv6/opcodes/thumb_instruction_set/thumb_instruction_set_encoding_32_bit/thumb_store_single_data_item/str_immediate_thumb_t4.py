from armulator.armv6.opcodes.abstract_opcodes.str_immediate_thumb import StrImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class StrImmediateThumbT4(StrImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        StrImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        wback = instr[23]
        add = instr[22]
        index = instr[21]
        rt = instr[16:20]
        rn = instr[12:16]
        if rn == "0b1111" or (not index and not wback):
            raise UndefinedInstructionException()
        elif rt.uint in (13, 15) or (wback and rn.uint == rt.uint):
            print "unpredictable"
        else:
            imm32 = zero_extend(imm8, 32)
            return StrImmediateThumbT4(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint,
                                                 "n": rn.uint, "imm32": imm32})
