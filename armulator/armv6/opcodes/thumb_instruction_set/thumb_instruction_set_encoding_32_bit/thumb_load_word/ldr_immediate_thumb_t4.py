from armulator.armv6.opcodes.abstract_opcodes.ldr_immediate_thumb import LdrImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class LdrImmediateThumbT4(LdrImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        wback = instr[23]
        add = instr[22]
        index = instr[21]
        rt = instr[16:20]
        rn = instr[12:16]
        if not index and not wback:
            raise UndefinedInstructionException()
        elif (wback and rn.uint == rt.uint) or (
                    rt.uint == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print("unpredictable")
        else:
            imm32 = zero_extend(imm8, 32)
            return LdrImmediateThumbT4(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint,
                                                 "n": rn.uint, "imm32": imm32})
