from armulator.armv6.opcodes.abstract_opcodes.cps_arm import CpsArm
from armulator.armv6.opcodes.opcode import Opcode


class CpsArmA1(CpsArm, Opcode):
    def __init__(self, instruction, affect_a, affect_i, affect_f, enable, disable, change_mode, mode):
        Opcode.__init__(self, instruction)
        CpsArm.__init__(self, affect_a, affect_i, affect_f, enable, disable, change_mode, mode)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mode = instr[27:32]
        f = instr[26]
        i = instr[25]
        a = instr[24]
        m = instr[14]
        imod = instr[12:14]
        if (mode != "0b00000" and not m) or (
                    (imod[0] and not (a or f or i)) or (not imod[0] and (a or f or i))) or (
                    (imod == "0b00" and not m) or imod == "0b01"):
            print("unpredictable")
        else:
            enable = imod == "0b10"
            disable = imod == "0b11"
            return CpsArmA1(instr, **{"affect_a": a, "affect_i": i, "affect_f": f, "enable": enable, "disable": disable,
                                      "change_mode": m, "mode": mode})
