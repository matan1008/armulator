from armulator.enums import DAbort


class EndOfInstruction(Exception):
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SVCException(Exception):
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DataAbortException(Exception):
    def __init__(self, abort_type):
        self.abort_type = abort_type

    def __str__(self):
        return repr(self.abort_type)

    def is_alignment_fault(self):
        return self.abort_type == DAbort.DAbort_Alignment


class HypTrapException(Exception):
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SMCException(Exception):
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UndefinedInstructionException(Exception):
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return repr(self.value)
