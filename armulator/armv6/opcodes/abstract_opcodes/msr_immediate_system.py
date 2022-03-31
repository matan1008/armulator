from armulator.armv6.opcodes.opcode import Opcode


class MsrImmediateSystem(Opcode):
    def __init__(self, instruction, write_spsr, mask, imm32):
        super().__init__(instruction)
        self.write_spsr = write_spsr
        self.mask = mask
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_spsr:
                processor.registers.spsr_write_by_instr(self.imm32, self.mask)
            else:
                processor.registers.cpsr_write_by_instr(self.imm32, self.mask, False)
                if processor.registers.cpsr.m == 0b11010 and processor.registers.cpsr.j and processor.registers.cpsr.t:
                    print('unpredictable')
