from armulator.shift import shift
from armulator.bits_ops import add
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction
from armulator.opcodes.abstract_opcode import AbstractOpcode


class LdrRegisterThumb(AbstractOpcode):
    def __init__(self, m, t, n, shift_t, shift_n):
        super(LdrRegisterThumb, self).__init__()
        self.m = m
        self.t = t
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(self.n)
            except EndOfInstruction:
                pass
            else:
                offset = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                               processor.registers.cpsr.get_c())
                offset_addr = add(processor.registers.get(self.n), offset, 32)
                address = offset_addr
                data = processor.mem_u_get(address, 4)
                if self.t == 15:
                    if address[30:32] == "0b00":
                        processor.load_write_pc(address)
                    else:
                        print "unpredictable"
                elif processor.unaligned_support() or address[30:32] == "0b00":
                    processor.registers.set(self.t, data)
                else:
                    processor.registers.set(self.t, BitArray(length=32))  # unknown
