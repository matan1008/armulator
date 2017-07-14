from armulator.armv6.opcodes.abstract_opcodes.ldm_thumb import LdmThumb
from armulator.armv6.opcodes.opcode import Opcode


class LdmThumbT1(LdmThumb, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        LdmThumb.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[8:16]
        rn = instr[5:8]
        registers = "0b00000000" + register_list
        wback = registers[15 - rn.uint]
        if registers.count(1) < 1:
            print "unpredictable"
        else:
            return LdmThumbT1(instr, **{"wback": wback, "registers": registers, "n": rn.uint})
