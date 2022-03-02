from armulator.armv6.opcodes.opcode import Opcode


class Sev(Opcode):
    def execute(self, processor):
        if processor.condition_passed():
            processor.send_event()
