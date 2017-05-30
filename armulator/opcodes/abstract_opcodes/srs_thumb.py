from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import UndefinedInstructionException
from armulator.bits_ops import add, sub
from bitstring import BitArray


class SrsThumb(AbstractOpcode):
    def __init__(self, increment, word_higher, wback, mode):
        super(SrsThumb, self).__init__()
        self.increment = increment
        self.word_higher = word_higher
        self.wback = wback
        self.mode = mode

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif processor.registers.current_mode_is_user_or_system():
                print "unpredictable"
            elif self.mode == "0b11010":
                print "unpredictable"
            else:
                if not processor.registers.is_secure():
                    if self.mode == "0b10110" or (self.mode == "0b10001" and processor.registers.nsacr.get_rfr()):
                        print "unpredictable"
                base = processor.registers.get_rmode(13, self.mode)
                address = base if self.increment else sub(base, BitArray(bin="1000"), 32)
                if self.word_higher:
                    address = add(address, BitArray(bin="100"), 32)
                processor.mem_a_set(address, 4, processor.registers.get_lr())
                processor.mem_a_set(add(address, BitArray(bin="100"), 32), 4, processor.registers.get_spsr())
                if self.wback:
                    processor.registers.set_rmode(
                            13,
                            self.mode,
                            (add(base, BitArray(bin="1000"), 32)
                             if self.increment
                             else sub(base, BitArray(bin="1000"), 32))
                    )
