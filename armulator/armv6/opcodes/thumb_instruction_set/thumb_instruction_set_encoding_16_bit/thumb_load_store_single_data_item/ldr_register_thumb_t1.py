from armulator.armv6.opcodes.abstract_opcodes.ldr_register_thumb import LdrRegisterThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import SRType


class LdrRegisterThumbT1(LdrRegisterThumb, Opcode):
    def __init__(self, instruction, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        LdrRegisterThumb.__init__(self, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.t == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[13:16]
        rn = instr[10:13]
        rm = instr[7:10]
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return LdrRegisterThumbT1(instr, **{"m": rm.uint, "t": rt.uint, "n": rn.uint, "shift_t": shift_t,
                                            "shift_n": shift_n})
