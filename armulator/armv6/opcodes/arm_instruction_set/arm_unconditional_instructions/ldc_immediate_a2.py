from armulator.armv6.opcodes.abstract_opcodes.ldc_immediate import LdcImmediate
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import sign_extend
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class LdcImmediateA2(LdcImmediate, Opcode):
    def __init__(self, instruction, cp, n, add, imm32, index, wback):
        Opcode.__init__(self, instruction)
        LdcImmediate.__init__(self, cp, n, add, imm32, index, wback)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        coproc = instr[20:24]
        rn = instr[12:16]
        index = instr[7]
        add = instr[8]
        wback = instr[10]
        if coproc[0:3] == "0b101":
            raise UndefinedInstructionException()
        else:
            imm32 = sign_extend(imm8 + "0b00", 32)
            return LdcImmediateA2(instr, **{"cp": coproc.uint, "n": rn.uint, "add": add, "imm32": imm32, "index": index,
                                            "wback": wback})
