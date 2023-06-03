import pickle, logging
from ..funcutils import get_function_id

from ..utils import create_temp_dir
from ..calltypes import Call, Return
from typing import Dict
import opcode

logger = logging.getLogger(__name__)

from .base import BaseCache

class MemCache(BaseCache):

    # this value is going to be used to help us keep track of a specific function, so we can join up a call and return object
    _call_id_cache: Dict[str, list]

    def __init__(self):
        super().__init__()
        self._call_id_cache = {}

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
        self._cache[obj.id].append(obj) 

    def ssave(self, invocation_id, obj):
        '''
        Save a call/return object to the cache
        Items saved in this manner are going to be stored in a (Call, Return) tuple so you can see exactly what the return values are for each call
        Also, this method is nice because you can run it with multithreading or whatever concurrency, and it will be fine

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

        if isinstance(obj, Return): 
            assert invocation_id in self._call_id_cache, "for some reason, we are trying to return from a function but we cant find the call object"
            self.__ensure_cache(obj.id)
            item = (self._call_id_cache[invocation_id], obj)
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
    

    @property
    def pretty_cache(self):
        '''
        Return a pretty version of the cache (basically stripping away the call and return objects)

        Returns:
            dict: the pretty cache
        '''

        pretty_cache = {}

        for key, value in self.cache.items():
            pretty_cache[key] = []


            for each in value:
                if isinstance(each, Return):
                    pretty_cache[key][''].append(each.retval)
                pretty_cache[key].append(each.args)

        return pretty_cache
    
    def get_cache_for_func(self, func_id):
        '''
        Given a function id (see get_function_id), return the cache for that function

        Args:
            func_id (str): the function id
        
        Returns:
            list: the cache for the function
        '''

        return self._cache[func_id]