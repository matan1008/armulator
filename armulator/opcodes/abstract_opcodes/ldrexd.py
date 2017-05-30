from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction


class Ldrexd(AbstractOpcode):
    def __init__(self, t, t2, n):
        super(Ldrexd, self).__init__()
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
                if address[29:32] != "0b000":
                    processor.alignment_fault(address, False)
                processor.set_exclusive_monitors(address, 8)
                processor.registers.set(self.t, processor.mem_a_get(address, 4))
                processor.registers.set(self.t2,
                                             processor.mem_a_get(BitArray(uint=address.uint + 4, length=32), 4))
