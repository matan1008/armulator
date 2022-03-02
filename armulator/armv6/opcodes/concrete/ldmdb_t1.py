from armulator.armv6.bits_ops import substring, chain, bit_at, bit_count
from armulator.armv6.opcodes.abstract_opcodes.ldmdb import Ldmdb


class LdmdbT1(Ldmdb):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 12, 0)
        p_m = substring(instr, 15, 14)
        wback = bit_at(instr, 21)
        rn = substring(instr, 19, 16)
        registers = chain(p_m, register_list, 14)
        if rn == 15 or bit_count(registers, 1, 16) < 2 or p_m == 0b11 or (
                bit_at(registers, 15) and processor.in_it_block() and not processor.last_in_it_block()) or (
                wback and bit_at(registers, rn)):
            print('unpredictable')
        else:
            return LdmdbT1(instr, wback=wback, registers=registers, n=rn)
