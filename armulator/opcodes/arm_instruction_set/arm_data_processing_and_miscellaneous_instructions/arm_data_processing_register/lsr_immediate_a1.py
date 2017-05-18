from armulator.opcodes.abstract_opcodes.lsr_immediate import LsrImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift
from bitstring import BitArray


class LsrImmediateA1(LsrImmediate, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_n):
        Opcode.__init__(self, instruction)
        LsrImmediate.__init__(self, setflags, m, d, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        imm5 = instr[20:25]
        rd = instr[16:20]
        s = instr[11]
        shift_t, shift_n = decode_imm_shift(BitArray(bin="01"), imm5)
        return LsrImmediateA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint,
                                        "shift_n": shift_n})
