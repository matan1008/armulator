from abc import ABC, abstractmethod


class AbstractOpcode(ABC):
    """
     Abstract Opcode class
    """

    @abstractmethod
    def __init__(self, **kw):
        pass

    @abstractmethod
    def execute(self, processor):
        """
        Execute the opcode on the given processor
        :param processor: Processor to run opcode on.
        """
        pass
