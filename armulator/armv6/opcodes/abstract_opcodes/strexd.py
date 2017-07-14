from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.armv6.arm_exceptions import EndOfInstruction


class Strexd(AbstractOpcode):
    def __init__(self, t, t2, d, n):
        super(Strexd, self).__init__()
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
                value = processor.registers.get(self.t) + processor.registers.get(
                        self.t2) if processor.big_endian() else processor.registers.get(
                    self.t2) + processor.registers.get(self.t)
                if processor.exclusive_monitors_pass(address, 4):
                    processor.mem_a_set(address, 8, value)
                    processor.registers.set(self.d, BitArray(bin="00000000000000000000000000000000"))
                else:
                    processor.registers.set(self.d, BitArray(bin="00000000000000000000000000000001"))
