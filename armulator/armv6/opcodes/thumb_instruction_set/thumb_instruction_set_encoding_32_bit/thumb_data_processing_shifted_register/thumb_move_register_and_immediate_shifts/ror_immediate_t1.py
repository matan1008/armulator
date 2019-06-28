from armulator.armv6.opcodes.abstract_opcodes.ror_immediate import RorImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift
from bitstring import BitArray


class RorImmediateT1(RorImmediate, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_n):
        Opcode.__init__(self, instruction)
        RorImmediate.__init__(self, setflags, m, d, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        setflags = instr[11]
        shift_t, shift_n = decode_imm_shift(BitArray(bin="11"), imm3 + imm2)
        if rd.uint in (13, 15) or rm.uint in (13, 15):
            print("unpredictable")
        else:
            return RorImmediateT1(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint, "shift_n": shift_n})
