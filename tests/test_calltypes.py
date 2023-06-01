from callcache.calltypes import Call, Return
import sys

def test_call():

    def a(x, y, z):
        mort = 23
        frame = sys._getframe(0)
        callobj = Call(frame)

        assert callobj.args == {'x': 1, 'y': 2, 'z': 3}
        assert callobj.frame == frame

    a(1,2,3)


    def b(x, y=2):
        meep = "a"
        frame = sys._getframe(0)
        callobj = Call(frame)

        assert callobj.args == {'x': 1, 'y': 2}

    b(1)

def test_ret():

    def handle_trace(frame, event, arg):
        if event == 'return':
            retobj = Return(frame, arg)
            assert retobj.retval == 3
            assert retobj.frame == frame
        elif event == 'call':
            return handle_trace 
        
    def a(x):
        return 3

    sys.settrace(handle_trace)
    a(1)
    sys.settrace(None)
