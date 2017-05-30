from armulator.opcodes.abstract_opcode import AbstractOpcode


class MsrRegisterApplication(AbstractOpcode):
    def __init__(self, write_nzcvq, write_g, n):
        super(MsrRegisterApplication, self).__init__()
        self.write_nzcvq = write_nzcvq
        self.write_g = write_g
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            temp_register = processor.core_registers.get(self.n)
            if self.write_nzcvq:
                processor.core_registers.cpsr.set_n(temp_register[0])
                processor.core_registers.cpsr.set_z(temp_register[1])
                processor.core_registers.cpsr.set_c(temp_register[2])
                processor.core_registers.cpsr.set_v(temp_register[3])
                processor.core_registers.cpsr.set_q(temp_register[4])
            if self.write_g:
                processor.core_registers.cpsr.set_ge(temp_register[12:16])
