import pickle, logging
from ..funcutils import get_function_id

from ..utils import create_temp_dir

logger = logging.getLogger(__name__)
cache_dir = create_temp_dir() 

def save_to_cache(type, value):
    file_id = get_function_id(value['frame'].f_code.co_filename, value['frame'].f_code.co_name)

    try:
        with open(f"{cache_dir}/{file_id}", 'rb') as f:
            cache = pickle.load(f)
    except:
        cache = {
            'arguments': [],
            'return_values': []
        }
        pass
    
    if type == "call":
        cache['arguments'].append(value['args'])
    elif type == "return":
        cache['return_values'].append(value['retval'])

    with open(f"{cache_dir}/{file_id}", 'wb') as f:
        pickle.dump(cache, f)


def get_cache_for_func_id(func_id):
    '''
    Given a function id (see get_function_id), return the cache for that function

    Args:
        file_name (str): the name of the file
        function_name (str): the name of the function

    Returns:
        dict: a dictionary containing the cache for the function
    
    Raises:
        Exception: if no cache exists for the function
    '''
    try:
        with open("cache/" + func_id, 'rb') as f:
            return pickle.load(f)
    except:
        raise Exception("No cache for function")
    

def list_args_for_func(func_id: str):
    '''
    Given a function id (see get_function_id), return the arguments that have been seen and cached

    Args:
        func_id (str): the function id

    Returns:
        list: a list of arguments that have been seen and cached 
    '''

    # given a filename and a function, list call arguments that have been seen and cached

    cache = get_cache_for_func_id(func_id)

    return cache['arguments']