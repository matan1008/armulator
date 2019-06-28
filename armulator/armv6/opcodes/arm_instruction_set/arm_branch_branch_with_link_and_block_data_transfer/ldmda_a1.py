from armulator.armv6.opcodes.abstract_opcodes.ldmda import Ldmda
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.configurations import arch_version


class LdmdaA1(Ldmda, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        Ldmda.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        rn = instr[12:16]
        wback = instr[10]
        if rn.uint == 15 or register_list.count(1) < 1 or (
                        wback and register_list[15 - rn.uint] and arch_version() >= 7):
            print("unpredictable")
        else:
            return LdmdaA1(instr, **{"wback": wback, "registers": register_list, "n": rn.uint})
