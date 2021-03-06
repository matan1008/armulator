from armulator.armv6.opcodes.abstract_opcodes.lsl_immediate import LslImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift
from bitstring import BitArray


class LslImmediateA1(LslImmediate, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_n):
        Opcode.__init__(self, instruction)
        LslImmediate.__init__(self, setflags, m, d, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        imm5 = instr[20:25]
        rd = instr[16:20]
        s = instr[11]
        shift_t, shift_n = decode_imm_shift(BitArray(bin="00"), imm5)
        return LslImmediateA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint,
                                        "shift_n": shift_n})
