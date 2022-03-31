from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.ldm_exception_return import LdmExceptionReturn


class LdmExceptionReturnA1(LdmExceptionReturn):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 15, 0)
        rn = substring(instr, 19, 16)
        increment = bit_at(instr, 23)
        word_higher = increment == bit_at(instr, 24)
        wback = bit_at(instr, 21)
        if rn == 15 or (wback and bit_at(register_list, rn) and arch_version() >= 7):
            print('unpredictable')
        else:
            return LdmExceptionReturnA1(instr, increment=increment, word_higher=word_higher, wback=wback,
                                        registers=register_list, n=rn)
