from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.asr_register import AsrRegister


class AsrRegisterT1(AsrRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        return AsrRegisterT1(instr, setflags=setflags, m=rm, d=rdn, n=rdn)
