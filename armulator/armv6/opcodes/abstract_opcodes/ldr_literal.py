from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align
from bitstring import BitArray
from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.shift import ror
from armulator.armv6.enums import InstrSet


class LdrLiteral(AbstractOpcode):
    def __init__(self, add, imm32, t):
        super(LdrLiteral, self).__init__()
        self.add = add
        self.imm32 = imm32
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(15)
            except EndOfInstruction:
                pass
            else:
                base = align(processor.registers.get_pc(), 4)
                address = bits_add(base, self.imm32, 32) if self.add else bits_sub(base, self.imm32, 32)
                data = processor.mem_u_get(address, 4)
                if self.t == 15:
                    if address[30:32] == "0b00":
                        processor.load_write_pc(data)
                    else:
                        print "unpredictable"
                elif processor.unaligned_support() or address[30:32] == "0b00":
                    processor.registers.set(self.t, data)
                else:
                    if processor.registers.current_instr_set() == InstrSet.InstrSet_ARM:
                        processor.registers.set(self.t, ror(data, 8 * address[30:32].uint))
                    else:
                        processor.registers.set(self.t, BitArray(length=32))  # unknown

    def instruction_syndrome(self):
        if self.t == 15:
            return BitArray(length=9)
        else:
            return BitArray(bin="11000") + BitArray(uint=self.t, length=4)
