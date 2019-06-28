from armulator.armv6.opcodes.abstract_opcodes.msr_register_system import MsrRegisterSystem
from armulator.armv6.opcodes.opcode import Opcode


class MsrRegisterSystemA1(MsrRegisterSystem, Opcode):
    def __init__(self, instruction, write_spsr, mask, n):
        Opcode.__init__(self, instruction)
        MsrRegisterSystem.__init__(self, write_spsr, mask, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        write_spsr = instr[9]
        mask = instr[12:16]
        if rn.uint == 15 or mask.bin == "0000":
            print("unpredictable")
        else:
            return MsrRegisterSystemA1(instr, **{"write_spsr": write_spsr, "mask": mask, "n": rn.uint})
