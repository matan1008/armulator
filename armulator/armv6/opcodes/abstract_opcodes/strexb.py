from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.armv6.arm_exceptions import EndOfInstruction


class Strexb(AbstractOpcode):
    def __init__(self, t, d, n):
        super(Strexb, self).__init__()
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
                    processor.mem_a_set(address, 1, processor.registers.get(self.t)[24:32])
                    processor.registers.set(self.d, BitArray(bin="00000000000000000000000000000000"))
                else:
                    processor.registers.set(self.d, BitArray(bin="00000000000000000000000000000001"))
