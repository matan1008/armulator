from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub, align
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction
from armulator.configurations import HaveLPAE


class LdrdLiteral(AbstractOpcode):
    def __init__(self, add, imm32, t, t2):
        super(LdrdLiteral, self).__init__()
        self.add = add
        self.imm32 = imm32
        self.t = t
        self.t2 = t2

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(15)
            except EndOfInstruction:
                pass
            else:
                address = bits_add(align(processor.registers.get_pc(), 4), self.imm32,
                                   32) if self.add else bits_sub(align(processor.registers.get_pc(), 4),
                                                                 self.imm32, 32)
                if HaveLPAE() and address[29:32] == "0b000":
                    data = processor.mem_a_get(address, 8)
                    if processor.big_endian():
                        processor.registers.set(self.t, data[0:32])
                        processor.registers.set(self.t2, data[32:64])
                    else:
                        processor.registers.set(self.t, data[32:64])
                        processor.registers.set(self.t2, data[0:32])
                else:
                    processor.registers.set(self.t, processor.mem_a_get(address, 4))
                    processor.registers.set(self.t2,
                                                 processor.mem_a_get(bits_add(address, BitArray(bin="0b000"), 32), 4))
