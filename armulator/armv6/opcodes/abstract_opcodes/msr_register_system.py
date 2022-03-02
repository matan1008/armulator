from armulator.armv6.opcodes.opcode import Opcode


class MsrRegisterSystem(Opcode):
    def __init__(self, instruction, write_spsr, mask, n):
        super().__init__(instruction)
        self.write_spsr = write_spsr
        self.mask = mask
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_spsr:
                processor.registers.spsr_write_by_instr(processor.registers.get(self.n), self.mask)
            else:
                processor.registers.cpsr_write_by_instr(processor.registers.get(self.n), self.mask, False)
                if processor.registers.cpsr.m == 0b11010 and processor.registers.cpsr.j and processor.registers.cpsr.t:
                    print('unpredictable')
