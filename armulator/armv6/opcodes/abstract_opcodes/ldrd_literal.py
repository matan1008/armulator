from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align, substring
from armulator.armv6.configurations import have_lpae
from armulator.armv6.opcodes.opcode import Opcode


class LdrdLiteral(Opcode):
    def __init__(self, instruction, add, imm32, t, t2):
        super().__init__(instruction)
        self.add = add
        self.imm32 = imm32
        self.t = t
        self.t2 = t2

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(15)
            except EndOfInstruction:
                pass
            else:
                pc = align(processor.registers.get_pc(), 4)
                address = bits_add(pc, self.imm32, 32) if self.add else bits_sub(pc, self.imm32, 32)
                if have_lpae() and substring(address, 2, 0) == 0b000:
                    data = processor.mem_a_get(address, 8)
                    if processor.big_endian():
                        processor.registers.set(self.t, substring(data, 63, 32))
                        processor.registers.set(self.t2, substring(data, 31, 0))
                    else:
                        processor.registers.set(self.t, substring(data, 31, 0))
                        processor.registers.set(self.t2, substring(data, 63, 32))
                else:
                    processor.registers.set(self.t, processor.mem_a_get(address, 4))
                    processor.registers.set(self.t2, processor.mem_a_get(bits_add(address, 4, 32), 4))
