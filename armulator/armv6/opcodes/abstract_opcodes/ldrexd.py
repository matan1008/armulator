from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.opcode import Opcode


class Ldrexd(Opcode):
    def __init__(self, instruction, t, t2, n):
        super().__init__(instruction)
        self.t = t
        self.t2 = t2
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                address = processor.registers.get(self.n)
                if substring(address, 2, 0) != 0b000:
                    processor.alignment_fault(address, False)
                processor.set_exclusive_monitors(address, 8)
                value = processor.mem_a_get(address, 8)
                if processor.big_endian():
                    processor.registers.set(self.t, substring(value, 63, 32))
                    processor.registers.set(self.t2, substring(value, 31, 0))
                else:
                    processor.registers.set(self.t, substring(value, 31, 0))
                    processor.registers.set(self.t2, substring(value, 63, 32))
