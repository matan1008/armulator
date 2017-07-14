from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import zero_extend


class Ldrexh(AbstractOpcode):
    def __init__(self, t, n):
        super(Ldrexh, self).__init__()
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
                processor.set_exclusive_monitors(address, 2)
                processor.registers.set(self.t, zero_extend(processor.mem_a_get(address, 2), 32))
