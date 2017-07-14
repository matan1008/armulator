from armulator.armv6.opcodes.abstract_opcodes.ldm_thumb import LdmThumb
from armulator.armv6.opcodes.opcode import Opcode


class LdmThumbT2(LdmThumb, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        LdmThumb.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[19:32]
        m = instr[17:18]
        p = instr[16:17]
        wback = instr[10]
        rn = instr[12:16]
        registers = p + m + "0b0" + register_list
        if rn.uint == 15 or registers.count(1) < 2 or (p == "0b1" and m == "0b1") or (
                        registers[0] and processor.in_it_block() and not processor.last_in_it_block()) or (
                    wback and registers[15 - rn.uint]):
            print "unpredictable"
        else:
            return LdmThumbT2(instr, **{"wback": wback, "registers": registers, "n": rn.uint})
