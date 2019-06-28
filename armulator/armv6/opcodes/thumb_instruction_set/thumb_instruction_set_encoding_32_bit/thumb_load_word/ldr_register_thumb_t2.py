from armulator.armv6.opcodes.abstract_opcodes.ldr_register_thumb import LdrRegisterThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import SRType


class LdrRegisterThumbT2(LdrRegisterThumb, Opcode):
    def __init__(self, instruction, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        LdrRegisterThumb.__init__(self, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        imm2 = instr[26:28]
        rt = instr[16:20]
        rn = instr[12:16]
        if rm.uint in (13, 15) or (rt.uint == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print("unpredictable")
        else:
            return LdrRegisterThumbT2(instr, **{"m": rm.uint, "t": rt.uint, "n": rn.uint,
                                                "shift_t": SRType.SRType_LSL, "shift_n": imm2.uint})
