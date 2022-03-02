from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class Udf(Opcode):
    def execute(self, processor):
        if processor.condition_passed():
            raise UndefinedInstructionException()
