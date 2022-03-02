from abc import ABC, abstractmethod


class Opcode(ABC):
    """
     Abstract Opcode class
    """

    def __init__(self, instruction):
        self.instruction = instruction

    @staticmethod
    def from_bitarray(instr, processor):
        pass

    @abstractmethod
    def execute(self, processor):
        """
        Execute the opcode on the given processor
        :param processor: Processor to run opcode on.
        """
        pass
