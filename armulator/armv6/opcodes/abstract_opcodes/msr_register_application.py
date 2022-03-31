from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.opcode import Opcode


class MsrRegisterApplication(Opcode):
    def __init__(self, instruction, write_nzcvq, write_g, n):
        super().__init__(instruction)
        self.write_nzcvq = write_nzcvq
        self.write_g = write_g
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            temp_register = processor.registers.get(self.n)
            if self.write_nzcvq:
                processor.registers.cpsr.n = bit_at(temp_register, 31)
                processor.registers.cpsr.z = bit_at(temp_register, 30)
                processor.registers.cpsr.c = bit_at(temp_register, 29)
                processor.registers.cpsr.v = bit_at(temp_register, 28)
                processor.registers.cpsr.q = bit_at(temp_register, 27)
            if self.write_g:
                processor.registers.cpsr.ge = substring(temp_register, 19, 16)
