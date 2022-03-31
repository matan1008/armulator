from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import sign_extend, bit_at, substring, bit_not, chain
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.abstract_opcodes.bl_blx_immediate import BlBlxImmediate


class BlBlxImmediateT2(BlBlxImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        h = bit_at(instr, 0)
        imm10l = substring(instr, 10, 1)
        j2 = bit_at(instr, 11)
        j1 = bit_at(instr, 13)
        imm10h = substring(instr, 25, 16)
        s = bit_at(instr, 26)
        i1 = bit_not(j1 ^ s, 1)
        i2 = bit_not(j2 ^ s, 1)
        imm32 = sign_extend(chain(s, chain(i1, chain(i2, chain(imm10h, imm10l << 2, 12), 22), 23), 24), 25, 32)
        target_instr_set = InstrSet.ARM
        if processor.registers.current_instr_set() == InstrSet.THUMB_EE or h:
            raise UndefinedInstructionException()
        elif processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return BlBlxImmediateT2(instr, target_instr_set=target_instr_set, imm32=imm32)
