from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import EndOfInstruction
from armulator.bits_ops import add


class Ldrex(AbstractOpcode):
    def __init__(self, imm32, t, n):
        super(Ldrex, self).__init__()
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
                address = add(processor.core_registers.get(self.n), self.imm32, 32)
                processor.set_exclusive_monitors(address, 4)
                processor.core_registers.set(self.t, processor.mem_a_get(address, 4))
