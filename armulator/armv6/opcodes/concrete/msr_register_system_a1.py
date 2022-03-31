from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.msr_register_system import MsrRegisterSystem


class MsrRegisterSystemA1(MsrRegisterSystem):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        write_spsr = bit_at(instr, 22)
        mask = substring(instr, 19, 16)
        if rn == 15 or mask == 0b0000:
            print('unpredictable')
        else:
            return MsrRegisterSystemA1(instr, write_spsr=write_spsr, mask=mask, n=rn)
