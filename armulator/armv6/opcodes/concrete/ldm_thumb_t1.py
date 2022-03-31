from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldm_thumb import LdmThumb


class LdmThumbT1(LdmThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        registers = substring(instr, 7, 0)
        rn = substring(instr, 10, 8)
        wback = bit_at(registers, rn) == 0
        if not registers:
            print('unpredictable')
        else:
            return LdmThumbT1(instr, wback=wback, registers=registers, n=rn)
