from armulator.armv6.opcodes.abstract_opcodes.pop_thumb import PopThumb
from armulator.armv6.opcodes.opcode import Opcode


class PopThumbT2(PopThumb, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        PopThumb.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[19:32]
        m = instr[17:18]
        p = instr[16:17]
        registers = p + m + "0b0" + register_list
        unaligned_allowed = False
        if registers.count(1) < 2 or (p == "0b1" and m == "0b1") or (
                        registers[0] and processor.in_it_block() and not processor.last_in_it_block()):
            print("unpredictable")
        else:
            return PopThumbT2(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
