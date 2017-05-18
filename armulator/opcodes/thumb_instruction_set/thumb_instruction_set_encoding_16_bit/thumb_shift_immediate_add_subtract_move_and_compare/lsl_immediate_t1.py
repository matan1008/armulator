from armulator.opcodes.abstract_opcodes.lsl_immediate import LslImmediate
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift
from bitstring import BitArray


class LslImmediateT1(LslImmediate, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_n):
        Opcode.__init__(self, instruction)
        LslImmediate.__init__(self, setflags, m, d, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm5 = instr[5:10]
        rd = instr[13:16]
        rm = instr[10:13]
        set_flags = not processor.in_it_block()
        shift_n = decode_imm_shift(BitArray(bin="00"), imm5)[1]
        return LslImmediateT1(instr, **{"setflags": set_flags, "m": rm.uint, "d": rd.uint, "shift_n": shift_n})
