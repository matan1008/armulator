from armulator.opcodes.abstract_opcodes.str_immediate_thumb import StrImmediateThumb
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class StrImmediateThumbT2(StrImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        StrImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        rt = instr[5:8]
        index = True
        add = True
        wback = False
        imm32 = zero_extend(imm8 + "0b00", 32)
        return StrImmediateThumbT2(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint, "n": 13,
                                             "imm32": imm32})
