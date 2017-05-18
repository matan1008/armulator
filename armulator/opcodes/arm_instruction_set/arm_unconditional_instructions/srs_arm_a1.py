from armulator.opcodes.abstract_opcodes.srs_arm import SrsArm
from armulator.opcodes.opcode import Opcode


class SrsArmA1(SrsArm, Opcode):
    def __init__(self, instruction, increment, word_higher, wback, mode):
        Opcode.__init__(self, instruction)
        SrsArm.__init__(self, increment, word_higher, wback, mode)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mode = instr[27:32]
        wback = instr[10]
        increment = instr[8]
        p = instr[7]
        word_higher = p == increment
        return SrsArmA1(instr, **{"increment": increment, "word_higher": word_higher, "wback": wback, "mode": mode})
