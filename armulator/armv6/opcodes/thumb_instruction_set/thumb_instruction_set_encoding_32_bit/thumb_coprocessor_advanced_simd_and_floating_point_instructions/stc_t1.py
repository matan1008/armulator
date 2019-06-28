from armulator.armv6.opcodes.abstract_opcodes.stc import Stc
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class StcT1(Stc, Opcode):
    def __init__(self, instruction, cp, n, add, imm32, index, wback):
        Opcode.__init__(self, instruction)
        Stc.__init__(self, cp, n, add, imm32, index, wback)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        coproc = instr[20:24]
        rn = instr[12:16]
        wback = instr[10]
        add = instr[8]
        index = instr[7]
        imm32 = zero_extend(imm8 + "0b00", 32)
        if instr[7:11] == "0b0000":
            raise UndefinedInstructionException()
        elif rn.uint == 15:
            print("unpredictable")
        else:
            return StcT1(instr, **{"cp": coproc.uint, "n": rn.uint, "add": add, "imm32": imm32, "index": index,
                                   "wback": wback})
