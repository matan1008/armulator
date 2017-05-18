from armulator.opcodes.abstract_opcodes.cps_thumb import CpsThumb
from armulator.opcodes.opcode import Opcode


class CpsThumbT2(CpsThumb, Opcode):
    def __init__(self, instruction, affect_a, affect_i, affect_f, enable, disable, change_mode, mode):
        Opcode.__init__(self, instruction)
        CpsThumb.__init__(self, affect_a, affect_i, affect_f, enable, disable, change_mode, mode)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mode = instr[27:32]
        affect_f = instr[26]
        affect_i = instr[25]
        affect_a = instr[24]
        change_mode = instr[23]
        imod = instr[21:23]
        enable = imod == "0b10"
        disable = imod == "0b11"
        if (mode != "0b00000" and not change_mode) or (
                            imod[0] and not affect_a and not affect_f and not affect_i) or (
                    not imod[0] and (affect_a or affect_i or affect_f)) or imod == "0b01" or processor.in_it_block():
            print "unpredictable"
        else:
            return CpsThumbT2(instr, **{"affect_a": affect_a, "affect_i": affect_i, "affect_f": affect_f,
                                        "enable": enable, "disable": disable, "change_mode": change_mode, "mode": mode})
