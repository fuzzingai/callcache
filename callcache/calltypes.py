import inspect 
from .funcutils import get_function_id
from types import FrameType
import logging
import traceback

logger = logging.getLogger(__name__)


from types import CodeType, FrameType
class SerializedFrame():
    def __init__(self, co_filename, co_name):
        self.f_code = CodeType(0, 0, 0, 0, 0, 0, b'', (), (), (), co_filename, co_name, 0, b'', (), ())


def _serialize_frame(frame: FrameType):
    '''
    By default, frame objects arent serializable, so we are going to attempt to create a new frame object that is serializable, and has the same accessors
    as the real frame object

    Args:
        frame (FrameType): the frame object to serialize

    Returns:
        SerializedFrame: a new frame object that is serializable
    '''

    # we need to create a new frame object that is serializable
    return SerializedFrame(frame.f_code.co_filename, frame.f_code.co_name) 

class BaseType:
    frame: FrameType

    @property
    def id(self):
        return (self.frame.f_code.co_filename, self.frame.f_code.co_name)
    
    @property 
    def filepath(self):
        return self.frame.f_code.co_filename
    
    @property
    def function_name(self):
        return self.frame.f_code.co_name

class Return(BaseType):
    def __init__(self, frame, retval):
        self.retval = retval 
        self.frame = frame
        logger.debug(f"Created Return object {self}")

    def __repr__(self):
        return f"Return(filepath={self.filepath}, function={self.function_name}, retval={self.retval})"

    # we mostly need to overwrite this method for testing purposes
    def __eq__(self, other):
        return self.retval == other.retval and self.frame == other.frame
    
    def __getstate__(self):
        return self.retval, _serialize_frame(self.frame)
    
    def __setstate__(self, state):
        self.retval, self.frame = state

class Call(BaseType):
    def __init__(self, frame):
        self.frame = frame
        argument_info = inspect.getargvalues(frame)
        arg_map = {}

        for each in argument_info.args:
            arg_map[each] = argument_info.locals[each]

        self.args = arg_map

        logger.debug(f"Created Call object {self}")
    
    def __repr__(self):
        return f"Call(filepath={self.filepath}, function={self.function_name}, args={self.args})"

    # we mostly need to overwrite this method for testing purposes
    def __eq__(self, other):
        return self.args == other.args and self.frame == other.frame
    
    def __getstate__(self):
        return self.args, _serialize_frame(self.frame)
    
    def __setstate__(self, state):
        self.args, self.frame = state
