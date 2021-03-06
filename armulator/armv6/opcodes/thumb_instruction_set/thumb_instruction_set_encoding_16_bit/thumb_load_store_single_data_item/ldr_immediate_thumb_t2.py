from armulator.armv6.opcodes.abstract_opcodes.ldr_immediate_thumb import LdrImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrImmediateThumbT2(LdrImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        rt = instr[5:8]
        index = True
        add = True
        wback = False
        imm32 = zero_extend(imm8 + "0b00", 32)
        return LdrImmediateThumbT2(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint, "n": 13,
                                             "imm32": imm32})
