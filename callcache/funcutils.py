import hashlib, logging

logger = logging.getLogger(__name__)

def get_function_id(file_name, function_name):
    '''
    Generates a function id via a md5 hash of the file name and function name

    Args:
        file_name (str): the name of the file
        function_name (str): the name of the function

    Returns:
        str: the md5 hash of the file name and function name
    '''
    return hashlib.md5(file_name.encode() + b":" + function_name.encode()).hexdigest()
