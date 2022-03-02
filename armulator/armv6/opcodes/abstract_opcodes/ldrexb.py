from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.opcodes.opcode import Opcode


class Ldrexb(Opcode):
    def __init__(self, instruction, t, n):
        super().__init__(instruction)
        self.t = t
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                address = processor.registers.get(self.n)
                processor.set_exclusive_monitors(address, 1)
                processor.registers.set(self.t, processor.mem_a_get(address, 1))
