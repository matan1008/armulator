from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.cdp_cdp2 import CdpCdp2


class CdpCdp2A1(CdpCdp2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        return CdpCdp2A1(instr, cp=coproc)
