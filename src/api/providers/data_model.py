from typing import Optional, TypeVar, List


T = TypeVar("T")

class DataModel:
    
    _data : List = []
    _output : List = []
    
    def __new__(cls, reset = False):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DataModel, cls).__new__(cls)
        
        if reset:
            cls._instance.reset()
            
        return cls._instance
    
    def append(self, item: T) -> None:
        self._data.append(item)
        
    def append_output_data(self, result, context = None) -> None:
        self._output.append(result)
    
    def delete(self, t) -> None:
        self._data = [x for x in self._data if x != t]
        return
    
    def initialize(self) -> None:
        self._data = []
        self._output = []
        
    def get_data(self, T) -> List:
        items = [x for x in self._data if type(x) == T]
        return items
    
    def get_response(self, T) -> List[T]:
        if type(T) == list:
            items = [
                x for x 
                in self._output 
                if type(x) == type(T) 
                     and len(T) > 0 
                     and len(x) > 0 
                     and type(x[0]) == T[0]
            ]
        else:
            items = [x for x in self._output if type(x) == T]
        return items or [[]]
    
    def reset(self):
        self._data = []
        self._output = []
    
    def set_data(self, data):
        self._data = data
        
    