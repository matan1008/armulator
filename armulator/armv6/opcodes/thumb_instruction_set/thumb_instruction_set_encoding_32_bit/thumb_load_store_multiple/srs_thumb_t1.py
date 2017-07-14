from armulator.armv6.opcodes.abstract_opcodes.srs_thumb import SrsThumb
from armulator.armv6.opcodes.opcode import Opcode


class SrsThumbT1(SrsThumb, Opcode):
    def __init__(self, instruction, word_higher, wback, mode):
        Opcode.__init__(self, instruction)
        SrsThumb.__init__(self, False, word_higher, wback, mode)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mode = instr[27:32]
        wback = instr[10]
        wordhigher = False
        return SrsThumbT1(instr, **{"word_higher": wordhigher, "wback": wback, "mode": mode})
