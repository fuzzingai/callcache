import pickle, logging
from ..funcutils import get_function_id

from ..utils import create_temp_dir
from ..calltypes import Call, Return
from typing import Dict

logger = logging.getLogger(__name__)

from .base import BaseCache

class MemCache(BaseCache):
    # this var is a mapping between the function id and the cache for calls/returns from and to that function
    cache = Dict

    def __init__(self):
        super().__init__()
        self.cache = {}

    def save(self, obj):
        '''
        Save a call/return object to the cache

        Args:
            obj (Call, Return): the call/return object to save to the cache
        
        Returns:
            None
        '''

        if not self.ensure_id_mapping(obj):
            logger.debug(f"Adding new function id mapping for {obj.id}")
            self.cache[obj.id] = []

        self.cache[obj.id].append(obj) 

    def get_full_cache(self):
        '''
        Return the full cache

        Returns:
            dict: the full cache
        '''
        return self.cache
    
    def get_cache_for_func(self, func_id):
        '''
        Given a function id (see get_function_id), return the cache for that function

        Args:
            func_id (str): the function id
        
        Returns:
            list: the cache for the function
        '''

        return self.cache[func_id]
    

    def get_pretty(self):
        mapping_dict = {}
        for hash, tuple in self.func_id_map.items():
            mapping_dict[tuple] = self.cache[hash]

        return mapping_dict