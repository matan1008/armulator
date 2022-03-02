from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align, chain, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class LdrhLiteral(Opcode):
    def __init__(self, instruction, add, imm32, t):
        super().__init__(instruction)
        self.add = add
        self.imm32 = imm32
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(15)
            except EndOfInstruction:
                pass
            else:
                base = align(processor.registers.get_pc(), 4)
                address = bits_add(base, self.imm32, 32) if self.add else bits_sub(base, self.imm32, 32)
                data = processor.mem_u_get(address, 2)
                if processor.unaligned_support() or not bit_at(address, 0):
                    processor.registers.set(self.t, data)
                else:
                    processor.registers.set(self.t, 0x00000000)  # unknown

    def instruction_syndrome(self):
        if self.t == 15:
            return 0b000000000
        else:
            return chain(0b10100, self.t, 4)
