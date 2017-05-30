from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add
from bitstring import BitArray
from armulator.arm_exceptions import EndOfInstruction


class PopThumb(AbstractOpcode):
    def __init__(self, registers, unaligned_allowed):
        super(PopThumb, self).__init__()
        self.registers = registers
        self.unaligned_allowed = unaligned_allowed

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(13)
            except EndOfInstruction:
                pass
            else:
                address = processor.registers.get_sp()
                for i in xrange(15):
                    if self.registers[15 - i]:
                        processor.registers.set(
                                i,
                                (processor.mem_u_get(address, 4)
                                 if self.unaligned_allowed
                                 else processor.mem_a_get(address, 4))
                        )
                        address = add(address, BitArray(bin="100"), 32)
                if self.registers[0]:
                    if self.unaligned_allowed:
                        if address[30:32] == "0b00":
                            processor.load_write_pc(processor.mem_u_get(address, 4))
                        else:
                            print "unpredictable"
                    else:
                        processor.load_write_pc(processor.mem_a_get(address, 4))
                if not self.registers[2]:
                    processor.registers.set_sp(
                            add(processor.registers.get_sp(),
                                BitArray(uint=(4 * self.registers.count(1)), length=32), 32))
                if self.registers[2]:
                    processor.registers.set_sp(BitArray(length=32))  # unknown
