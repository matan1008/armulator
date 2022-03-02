from armulator.armv6.opcodes.opcode import Opcode


class Yield(Opcode):
    def execute(self, processor):
        if processor.condition_passed():
            processor.hint_yield()
