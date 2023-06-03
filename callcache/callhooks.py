import inspect, logging
from .cache.mem import MemCache
from .calltypes import Call, Return
from .tracefilters import Filter
import time

logger = logging.getLogger(__name__)

# a function that generates a 20 digit unique id
# this is used to identify the function that we are currently in
def get_unique_id():
    return id(time.time())

def stracer(cache, filters: Filter):
    '''
    This is the version of the tracer that will use the ssave function of the cache
    You probably want to use this
    '''

    def handle_return(call_id):
        def r(frame, event, arg):
            if event == 'return':
                e = Return(frame=frame, retval=arg)
                logger.info(f"Returning from {e}")
                cache.ssave(call_id, e)

        return r

    def handle_call(frame, event, arg):
        if event == 'call':
            if not filters.keep_frame(frame):
                return

            e = Call(frame=frame)
            call_id = get_unique_id()
            # for this new frame, only trace exceptions and returns
            logger.info(f"Entering {e}")
            frame.f_trace_lines = False
            cache.ssave(call_id, e)
            return handle_return(call_id) 

    return handle_call 

def tracer(cache, filters: Filter):
    '''
    The main callback to the sys.settrace function
    This function is called for every event in the program, but it has a filter on it so that it should only handle events for the files that we are watching
    The file watch list is set by the set_watch_files function
    '''
    def handle_settrace(frame, event, arg):
        if not filters.keep_frame(frame):
            return

        if event == 'call':
            e = Call(frame=frame)
            # for this new frame, only trace exceptions and returns
            logger.info(f"Entering {e}")
            frame.f_trace_lines = False
            cache.save(e)
            return handle_settrace 
        elif event == 'return':
            e = Return(frame=frame, retval=arg)
            logger.info(f"Returning from {e}")
            cache.save(e)

    return handle_settrace

# father forgive me for I have sinned
# this just sets a global variable
def set_watch_files(files):
    '''
    A function that sets the files that we are watching.
    Sets a global variable that is used by the tracer function
    '''

    global watch_files
    watch_files = files

def memtracer(frame, event, arg):
    '''
    The main callback to the sys.settrace function
    This function is called for every event in the program, but it has a filter on it so that it should only handle events for the files that we are watching
    The file watch list is set by the set_watch_files function
    '''
    global watch_files

    if not (frame.f_code.co_filename in watch_files):
        return 

    if event == 'call':
        # for this new frame, only trace exceptions and returns
        handle_call(frame, event, arg, MemCache())
        return memtracer 
    elif event == 'return':
        handle_ret(frame, event, arg)


