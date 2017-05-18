from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction


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
                address = processor.core_registers.get(self.n)
                value = processor.core_registers.get(self.t) + processor.core_registers.get(
                        self.t2) if processor.big_endian() else processor.core_registers.get(
                    self.t2) + processor.core_registers.get(self.t)
                if processor.exclusive_monitors_pass(address, 4):
                    processor.mem_a_set(address, 8, value)
                    processor.core_registers.set(self.d, BitArray(bin="00000000000000000000000000000000"))
                else:
                    processor.core_registers.set(self.d, BitArray(bin="00000000000000000000000000000001"))
