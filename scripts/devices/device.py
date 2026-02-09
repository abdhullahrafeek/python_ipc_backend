from abc import ABC, abstractmethod
from services import AsyncRuntime

from state import SharedState

class Device(ABC):
    def __init__(self, name, type, shared_state: SharedState):
        self.name = name
        self.stream = shared_state.register_stream(name, type)
        self._start()

    def __aiter__(self):
        return self
    
    async def __anext__(self):
        return await AsyncRuntime.run_in_executor(self._read)
    
    @abstractmethod
    def _read(self):
        '''
        Docstring for _read
        Implement the proper read function
        
        :param self: self
        '''
        pass

    @abstractmethod
    async def process_output(self, data) -> bool:
        '''
        Docstring for process_output
        Implement how the output should be processed
        
        :param self: self
        :param data: data to be processed
        :return: Success or Failure
        :rtype: bool
        '''
        pass

    @abstractmethod
    def close(self):
        '''
        Docstring for close
        Implement any closing operation
        
        :param self: Description
        '''
        pass

    @abstractmethod
    def _start(self):
        pass