from abc import ABC, abstractmethod

class Backend(ABC):
    
    @abstractmethod
    def execute(self, task):
        pass