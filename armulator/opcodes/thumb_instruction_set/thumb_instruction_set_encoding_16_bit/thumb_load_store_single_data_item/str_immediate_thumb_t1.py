from armulator.opcodes.abstract_opcodes.str_immediate_thumb import StrImmediateThumb
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class StrImmediateThumbT1(StrImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        StrImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[13:16]
        rn = instr[10:13]
        imm5 = instr[5:10]
        index = True
        add = True
        wback = False
        imm32 = zero_extend(imm5 + "0b00", 32)
        return StrImmediateThumbT1(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint, "n": rn.uint,
                                             "imm32": imm32})
