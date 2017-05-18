from abc import ABCMeta, abstractmethod
from bitstring import BitArray
from armulator.opcodes.abstract_opcode import AbstractOpcode


class Opcode(AbstractOpcode):
    """
     Abstract Opcode class
    """
    __metaclass__ = ABCMeta

    def __init__(self, instruction=BitArray()):
        super(Opcode, self).__init__()
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
        return self.instruction_length() / 8

    @staticmethod
    def from_bitarray(instr, processor):
        raise NotImplementedError()
