import logging
from ..funcutils import get_function_id
import dill as pickle
from IPython import embed

from ..utils import create_temp_dir
from ..calltypes import Call, Return
from typing import Dict, Tuple, List
import opcode

logger = logging.getLogger(__name__)

from .base import BaseCache

class MemCache(BaseCache):
    def __init__(self):
        super().__init__()
        # this value is going to be used to help us keep track of a specific function, so we can join up a call and return object
        self._call_id_cache: Dict[Tuple, List] = {}

    def __getstate__(self):
        return self._cache

    def __setstate__(self, state):
        self._cache = state

    def __ensure_cache(self, func_id):
        if func_id not in self.cache:
            logger.debug(f"Adding new function id mapping for {func_id}")
            self._cache[func_id] = []

    def save(self, obj):
        '''
        Save a call/return object to the cache

        Args:
            obj (Call, Return): the call/return object to save to the cache
        
        Returns:
            None
        '''

        self.__ensure_cache(obj.id)
        logger.debug(f"Inserting new item into cache from save: {obj}")
        self._cache[obj.id].append(obj) 

    def buffered_call_return_save(self, invocation_id, obj):
        '''
        Save a call/return object to the cache
        Items saved in this manner are going to be stored in a {'call': Call, 'return': Return} dict so you can see exactly what the return values are for each call
        Also, this method is nice because you can run it with multithreading or whatever concurrency, and it will be fine. The only time that things get added to the cache 
        with this method is when both the call and return objects are present, so be conscious of that

        Args:
            invocation_id (str): a unique id to the particular invocation of a function. This value should be the same when the call and return values of the same instance of a function invocation are performed
            obj (Call, Return): the call/return object to save to the cache
        
        Returns:
            None

        Raises:
            AssertionError
        '''

        if isinstance(obj, Call):
            assert invocation_id not in self._call_id_cache, "Got invocation_id collision!"
            logger.debug(f"Adding new invocation id mapping for {invocation_id}")
            self._call_id_cache[invocation_id] = obj

        elif isinstance(obj, Return): 
            assert invocation_id in self._call_id_cache, "for some reason, we are trying to return from a function but we cant find the call object"
            self.__ensure_cache(obj.id)
            item = {
                'call': self._call_id_cache[invocation_id], 
                'return': obj
            }
            self._cache[obj.id].append(item)
            logger.debug(f"Inserting new item into cache: {item}")
            del self._call_id_cache[invocation_id] 
            logger.debug(f"Deleting invocation id mapping for {invocation_id}")


    @property
    def cache(self):
        '''
        Return the full cache

        Returns:
            dict: the full cache
        '''
        return self._cache
    
    
    def get_cache_for_func(self, func_id):
        '''
        Given a function id (see get_function_id), return the cache for that function

        Args:
            func_id (str): the function id
        
        Returns:
            list: the cache for the function
        '''

        return self._cache[func_id]
    

    def save_to_file(self, filename: str):
        '''
        Save the cache to a file

        Args:
            filename (str): the filename to save the cache to

        Returns:
            None
        '''

        with open(filename, 'wb') as f:
            pickle.dump(self, f)