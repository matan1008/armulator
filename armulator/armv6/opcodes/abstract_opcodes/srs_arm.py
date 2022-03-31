from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import add, sub
from armulator.armv6.opcodes.opcode import Opcode


class SrsArm(Opcode):
    def __init__(self, instruction, increment, word_higher, wback, mode):
        super().__init__(instruction)
        self.increment = increment
        self.word_higher = word_higher
        self.wback = wback
        self.mode = mode

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif processor.registers.current_mode_is_user_or_system():
                print('unpredictable')
            elif self.mode == 0b11010:
                print('unpredictable')
            else:
                if not processor.registers.is_secure():
                    if self.mode == 0b10110 or (self.mode == 0b10001 and processor.registers.nsacr.rfr):
                        print('unpredictable')
                base = processor.registers.get_rmode(13, self.mode)
                address = base if self.increment else sub(base, 8, 32)
                if self.word_higher:
                    address = add(address, 4, 32)
                processor.mem_a_set(address, 4, processor.registers.get_lr())
                processor.mem_a_set(add(address, 4, 32), 4, processor.registers.get_spsr())
                if self.wback:
                    processor.registers.set_rmode(
                        13, self.mode, add(base, 8, 32) if self.increment else sub(base, 8, 32)
                    )
