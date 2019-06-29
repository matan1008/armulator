from abc import ABCMeta, abstractmethod


class Opcode(object):
    """
     Abstract Opcode class
    """
    __metaclass__ = ABCMeta

    def __init__(self, instruction):
        self.instruction = instruction

    @abstractmethod
    def is_pc_changing_opcode(self):
        """ For knowin whether to increment PC or not """
        pass

    def instruction_length(self):
        """ Length in Bits"""
        return self.instruction.len

    def bytes_len(self):
        """ Length in Bytes """
        return self.instruction_length() // 8

    @staticmethod
    def from_bitarray(instr, processor):
        raise NotImplementedError()
