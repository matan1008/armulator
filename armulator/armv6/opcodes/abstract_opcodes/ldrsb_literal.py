from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align, sign_extend, chain
from armulator.armv6.opcodes.opcode import Opcode


class LdrsbLiteral(Opcode):
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
                processor.registers.set(self.t, sign_extend(processor.mem_u_get(address, 1), 8, 32))

    def instruction_syndrome(self):
        if self.t == 15:
            return 0b000000000
        else:
            return chain(0b10010, self.t, 4)
