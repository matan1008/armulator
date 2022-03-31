from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.cdp_cdp2 import CdpCdp2


class CdpCdp2T2(CdpCdp2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        if substring(coproc, 3, 1) == 0b101:
            raise UndefinedInstructionException()
        else:
            return CdpCdp2T2(instr, cp=coproc)
