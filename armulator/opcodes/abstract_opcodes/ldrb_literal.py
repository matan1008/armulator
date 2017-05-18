from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub, zero_extend, align
from armulator.arm_exceptions import EndOfInstruction


class LdrbLiteral(AbstractOpcode):
    def __init__(self, add, imm32, t):
        super(LdrbLiteral, self).__init__()
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
                base = align(processor.core_registers.get_pc(), 4)
                address = bits_add(base, self.imm32, 32) if self.add else bits_sub(base, self.imm32, 32)
                processor.core_registers.set(self.t, zero_extend(processor.mem_u_get(address, 1), 32))
