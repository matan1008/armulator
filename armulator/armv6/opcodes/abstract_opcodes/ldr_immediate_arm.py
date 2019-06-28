from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub
from armulator.armv6.shift import ror
from bitstring import BitArray


class LdrImmediateArm(AbstractOpcode):
    def __init__(self, add, wback, index, t, n, imm32):
        super(LdrImmediateArm, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.t = t
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                    processor.registers.get(self.n), self.imm32, 32)
            address = offset_addr if self.index else processor.registers.get(self.n)
            data = processor.mem_u_get(address, 4)
            if self.wback:
                processor.registers.set(self.n, offset_addr)
            if self.t == 15:
                if address[30:32] == "0b00":
                    processor.load_write_pc(data)
                else:
                    print("unpredictable")
            elif processor.unaligned_support() or address[30:32] == "0b00":
                processor.registers.set(self.t, data)
            else:
                processor.registers.set(self.t, ror(data, 8 * address[30:32].uint))

    def instruction_syndrome(self):
        if self.t == 15 or self.wback:
            return BitArray(length=9)
        else:
            return BitArray(bin="11000") + BitArray(uint=self.t, length=4)
