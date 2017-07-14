from armulator.armv6.opcodes.abstract_opcodes.cdp import Cdp
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class CdpA2(Cdp, Opcode):
    def __init__(self, instruction, cp):
        Opcode.__init__(self, instruction)
        Cdp.__init__(self, cp)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        if coproc[0:3] == "0b101":
            raise UndefinedInstructionException()
        else:
            return CdpA2(instr, **{"cp": coproc.uint})
