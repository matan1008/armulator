from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add


class Ldrex(Opcode):
    def __init__(self, instruction, imm32, t, n):
        super().__init__(instruction)
        self.imm32 = imm32
        self.t = t
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                address = add(processor.registers.get(self.n), self.imm32, 32)
                processor.set_exclusive_monitors(address, 4)
                processor.registers.set(self.t, processor.mem_a_get(address, 4))
