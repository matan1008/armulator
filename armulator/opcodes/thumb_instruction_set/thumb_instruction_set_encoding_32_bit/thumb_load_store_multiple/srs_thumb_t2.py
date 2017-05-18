from armulator.opcodes.abstract_opcodes.srs_thumb import SrsThumb
from armulator.opcodes.opcode import Opcode


class SrsThumbT2(SrsThumb, Opcode):
    def __init__(self, instruction, word_higher, wback, mode):
        Opcode.__init__(self, instruction)
        SrsThumb.__init__(self, True, word_higher, wback, mode)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mode = instr[27:32]
        wback = instr[10]
        wordhigher = False
        return SrsThumbT2(instr, **{"word_higher": wordhigher, "wback": wback, "mode": mode})
