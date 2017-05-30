from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction
from armulator.bits_ops import add


class Strex(AbstractOpcode):
    def __init__(self, imm32, t, d, n):
        super(Strex, self).__init__()
        self.imm32 = imm32
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
                address = add(processor.registers.get(self.n), self.imm32, 32)
                if processor.exclusive_monitors_pass(address, 4):
                    processor.mem_a_set(address, 4, processor.registers.get(self.t))
                    processor.registers.set(self.d, BitArray(bin="00000000000000000000000000000000"))
                else:
                    processor.registers.set(self.d, BitArray(bin="00000000000000000000000000000001"))
