from armulator.opcodes.abstract_opcodes.cps_thumb import CpsThumb
from armulator.opcodes.opcode import Opcode


class CpsThumbT1(CpsThumb, Opcode):
    def __init__(self, instruction, affect_a, affect_i, affect_f, enable, disable):
        Opcode.__init__(self, instruction)
        CpsThumb.__init__(self, affect_a, affect_i, affect_f, enable, disable, False)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        affect_a = instr[13]
        affect_i = instr[14]
        affect_f = instr[15]
        enable = not instr[11]
        disable = instr[11]
        if (not affect_a and not affect_i and not affect_f) or processor.in_it_block():
            print "unpredictable"
        else:
            return CpsThumbT1(instr, **{"affect_a": affect_a, "affect_i": affect_i, "affect_f": affect_f,
                                        "enable": enable, "disable": disable})
