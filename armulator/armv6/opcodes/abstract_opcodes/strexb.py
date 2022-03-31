from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import lower_chunk
from armulator.armv6.opcodes.opcode import Opcode


class Strexb(Opcode):
    def __init__(self, instruction, t, d, n):
        super().__init__(instruction)
        self.t = t
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                address = processor.registers.get(self.n)
                if processor.exclusive_monitors_pass(address, 1):
                    processor.mem_a_set(address, 1, lower_chunk(processor.registers.get(self.t), 8))
                    processor.registers.set(self.d, 0b00000000000000000000000000000000)
                else:
                    processor.registers.set(self.d, 0b00000000000000000000000000000001)
