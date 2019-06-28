from armulator.armv6.opcodes.abstract_opcodes.msr_register_system import MsrRegisterSystem
from armulator.armv6.opcodes.opcode import Opcode


class MsrRegisterSystemT1(MsrRegisterSystem, Opcode):
    def __init__(self, instruction, write_spsr, mask, n):
        Opcode.__init__(self, instruction)
        MsrRegisterSystem.__init__(self, write_spsr, mask, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mask = instr[20:24]
        rn = instr[12:16]
        write_spsr = instr[11]
        if mask == "0b0000" or rn.uint in (13, 15):
            print("unpredictable")
        else:
            return MsrRegisterSystemT1(instr, **{"write_spsr": write_spsr, "mask": mask, "n": rn.uint})
