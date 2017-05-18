from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import UndefinedInstructionException


class Udf(AbstractOpcode):
    def __init__(self):
        super(Udf, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            raise UndefinedInstructionException()
