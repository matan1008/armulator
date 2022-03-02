from armulator.armv6.bits_ops import sign_extend, substring, bit_at, chain
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.abstract_opcodes.bl_blx_immediate import BlBlxImmediate


class BlBlxImmediateA2(BlBlxImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm24 = substring(instr, 23, 0)
        h = bit_at(instr, 24)
        imm32 = sign_extend(chain(imm24, h, 1) << 1, 26, 32)
        target_instrset = InstrSet.THUMB
        return BlBlxImmediateA2(instr, target_instr_set=target_instrset, imm32=imm32)
