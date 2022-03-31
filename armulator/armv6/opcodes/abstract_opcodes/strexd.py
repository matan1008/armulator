from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import chain
from armulator.armv6.opcodes.opcode import Opcode


class Strexd(Opcode):
    def __init__(self, instruction, t, t2, d, n):
        super().__init__(instruction)
        self.t = t
        self.t2 = t2
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
                t = processor.registers.get(self.t)
                t2 = processor.registers.get(self.t2)
                value = chain(t, t2, 32) if processor.big_endian() else chain(t2, t, 32)
                if processor.exclusive_monitors_pass(address, 4):
                    processor.mem_a_set(address, 8, value)
                    processor.registers.set(self.d, 0b00000000000000000000000000000000)
                else:
                    processor.registers.set(self.d, 0b00000000000000000000000000000001)
