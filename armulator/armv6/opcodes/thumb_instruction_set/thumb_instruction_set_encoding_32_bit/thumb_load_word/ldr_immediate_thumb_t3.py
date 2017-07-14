from armulator.armv6.opcodes.abstract_opcodes.ldr_immediate_thumb import LdrImmediateThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrImmediateThumbT3(LdrImmediateThumb, Opcode):
    def __init__(self, instruction, add, wback, index, t, n, imm32):
        Opcode.__init__(self, instruction)
        LdrImmediateThumb.__init__(self, add, wback, index, t, n, imm32)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        index = True
        add = True
        wback = False
        imm12 = instr[20:32]
        rt = instr[16:20]
        rn = instr[12:16]
        imm32 = zero_extend(imm12, 32)
        if rt.uint == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return LdrImmediateThumbT3(instr, **{"add": add, "wback": wback, "index": index, "t": rt.uint,
                                                 "n": rn.uint, "imm32": imm32})
