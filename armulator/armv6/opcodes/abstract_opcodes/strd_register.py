from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub
from bitstring import BitArray
from armulator.armv6.configurations import have_lpae


class StrdRegister(AbstractOpcode):
    def __init__(self, add, wback, index, m, t, t2, n):
        super(StrdRegister, self).__init__()
        self.add = add
        self.wback = wback
        self.index = index
        self.m = m
        self.t = t
        self.t2 = t2
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            offset_addr = bits_add(processor.registers.get(self.n), processor.registers.get(self.m),
                                   32) if self.add else bits_sub(processor.registers.get(self.n),
                                                                 processor.registers.get(self.m), 32)
            address = offset_addr if self.index else processor.registers.get(self.n)
            if have_lpae() and address[29:32] == "0b000":
                if processor.big_endian():
                    data = processor.registers.get(self.t) + processor.registers.get(self.t2)
                else:
                    data = processor.registers.get(self.t2) + processor.registers.get(self.t)
                processor.mem_a_set(address, 8, data)
            else:
                processor.mem_a_set(address, 4, processor.registers.get(self.t))
                processor.mem_a_set(bits_add(address, BitArray(bin="100"), 32), 4,
                                    processor.registers.get(self.t2))
            if self.wback:
                processor.registers.set(self.n, offset_addr)
