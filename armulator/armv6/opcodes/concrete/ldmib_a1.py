from armulator.armv6.bits_ops import substring, bit_at, bit_count
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.ldmib import Ldmib


class LdmibA1(Ldmib):
    @staticmethod
    def from_bitarray(instr, processor):
        registers = substring(instr, 15, 0)
        rn = substring(instr, 19, 16)
        wback = bit_at(instr, 21)
        if rn == 15 or bit_count(registers, 1, 16) < 1 or (wback and bit_at(registers, rn) and arch_version() >= 7):
            print('unpredictable')
        else:
            return LdmibA1(instr, wback=wback, registers=registers, n=rn)
