from abc import abstractmethod
from ..calltypes import BaseType
from typing import Dict

class BaseCache:
    def __init__(self):
        # this value is a mapping between a function id given by the get_function_id function and a tuple of the file name and function name
        self._cache: Dict[tuple, Dict] = {}

    @abstractmethod
    def cache(self):
        pass

    @abstractmethod
    def pretty_cache(self):
        '''
        Return a pretty version of the cache (basically stripping away the call and return objects)
        '''
        pass

    @abstractmethod
    def save(self, obj):
        pass