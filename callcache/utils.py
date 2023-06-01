import os, random, string

def create_temp_dir():
    ''' 
    A function that creates a temporary directory in /tmp, with a random 15 character name

    Args:
        None

    Returns:
        str: the name of the directory created
    '''
    dirname = '/tmp/' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    os.mkdir(dirname)
    return dirname