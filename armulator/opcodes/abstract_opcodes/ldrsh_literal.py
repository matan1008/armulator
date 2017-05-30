from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub, sign_extend, align
from armulator.arm_exceptions import EndOfInstruction
from bitstring import BitArray


class LdrshLiteral(AbstractOpcode):
    def __init__(self, add, imm32, t):
        super(LdrshLiteral, self).__init__()
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
                data = processor.mem_u_get(address, 2)
                if processor.unaligned_support() or not address[31]:
                    processor.registers.set(self.t, sign_extend(data, 32))
                else:
                    processor.registers.set(self.t, BitArray(length=32))  # unkown
