from armulator.armv6.enums import DAbort

__all__ = ['ArmulatorException', 'EndOfInstruction', 'SVCException', 'DataAbortException', 'HypTrapException',
           'SMCException', 'UndefinedInstructionException']


class ArmulatorException(Exception):
    """ Domain exception for armulator errors. """
    pass


class EndOfInstruction(ArmulatorException):
    def __str__(self):
        return repr(self.args[0])


class SVCException(ArmulatorException):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DataAbortException(ArmulatorException):
    def __init__(self, abort_type, is_second_stage):
        self.abort_type = abort_type
        self.is_second_stage = is_second_stage

    def __str__(self):
        return repr(self.abort_type)

    def is_alignment_fault(self):
        return self.abort_type == DAbort.ALIGNMENT

    def second_stage_abort(self):
        return self.is_second_stage


class HypTrapException(ArmulatorException):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SMCException(ArmulatorException):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UndefinedInstructionException(ArmulatorException):
    def __str__(self):
        return repr(self.args[0])
