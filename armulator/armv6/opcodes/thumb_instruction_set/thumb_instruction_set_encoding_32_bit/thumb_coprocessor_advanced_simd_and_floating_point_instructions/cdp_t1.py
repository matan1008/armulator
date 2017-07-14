from armulator.armv6.opcodes.abstract_opcodes.cdp import Cdp
from armulator.armv6.opcodes.opcode import Opcode


class CdpT1(Cdp, Opcode):
    def __init__(self, instruction, cp):
        Opcode.__init__(self, instruction)
        Cdp.__init__(self, cp)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        return CdpT1(instr, **{"cp": coproc.uint})
