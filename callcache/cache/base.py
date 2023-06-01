from abc import abstractmethod
from ..calltypes import BaseType
from typing import Dict

class BaseCache:
    # this value is a mapping between a function id given by the get_function_id function and a tuple of the file name and function name
    func_id_map: Dict[str, tuple]

    def __init__(self):
        self.func_id_map = {}

    @property
    def id_map(self):
        return self.func_id_map

    def ensure_id_mapping(self, t: BaseType):
        '''
        Ensure that the function id mapping to the file name and function name exists.
        If the given object was not previously seen, then add it to the mapping

        Args:
            t (BaseType): the call/return object to ensure the mapping for

        Returns:
            bool: True if the mapping already existed, False otherwise
        '''

        if t.id not in self.func_id_map.keys():
            self.func_id_map[t.id] = (t.filepath, t.function_name)
            return False
        
        return True
        
    @staticmethod
    @abstractmethod
    def save_call(value):
        pass

    @staticmethod
    @abstractmethod
    def save_return(value):
        pass