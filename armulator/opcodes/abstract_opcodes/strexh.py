from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction


class Strexh(AbstractOpcode):
    def __init__(self, t, d, n):
        super(Strexh, self).__init__()
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
                address = processor.core_registers.get(self.n)
                if processor.exclusive_monitors_pass(address, 2):
                    processor.mem_a_set(address, 2, processor.core_registers.get(self.t)[16:32])
                    processor.core_registers.set(self.d, BitArray(bin="00000000000000000000000000000000"))
                else:
                    processor.core_registers.set(self.d, BitArray(bin="00000000000000000000000000000001"))
