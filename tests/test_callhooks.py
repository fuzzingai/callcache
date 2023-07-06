from callcache.cache.mem import MemCache
from callcache.callhooks import tracer, stracer
from callcache.calltypes import Call, Return
from callcache.tracefilters import FileFilter, FunctionNameFilter
import sys, logging, pprint
from IPython import embed

def test_settrace_handler(caplog):
    mc = MemCache()
    stuff = []

    def one(a, b):
        c = a * b
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=c))
        return c

    f = FileFilter(__file__) & FunctionNameFilter("one")

    assert mc.get_full_cache() == {}

    sys.settrace(tracer(mc, f))
    one(1,2)
    sys.settrace(None)

    assert mc.cache != {}
    assert mc.get_cache_for_func(stuff[0].id) == stuff

    assert mc.get_full_cache() == {
        stuff[0].id: stuff
    }

def test_settrace_handler(caplog):
    mc = MemCache()
    stuff = []

    def one(a, b):
        c = a * b
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=c))
        return c

    def two(x, y, z):
        memo = x + 2 * y * z
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=memo))
        return memo

    ### Test 1
    f = FileFilter(__file__) & FunctionNameFilter("one")

    assert mc.cache == {}

    sys.settrace(tracer(mc, f))
    one(1,2)
    two(1,2,3)
    sys.settrace(None)

    assert mc.cache != {}
    assert mc.get_cache_for_func(stuff[0].id) == stuff[0:2]

    assert stuff[2].id not in mc.cache

def test_settrace_handler2():
    ### Test 2
    f = FileFilter(__file__) | FunctionNameFilter("two")
    mc = MemCache()
    stuff = []
    def one(a, b):
        c = a * b
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=c))
        return c

    def two(x, y, z):
        memo = x + 2 * y * z
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=memo))
        return memo

    sys.settrace(tracer(mc, f))
    one(1,2)
    two(1,2,3)
    sys.settrace(None)    

    assert mc.get_cache_for_func(stuff[0].id) == stuff[0:2]
    assert mc.get_cache_for_func(stuff[2].id) == stuff[2:4]

def test_settrace_handler3():
    f = FunctionNameFilter(include=["two"], exclude=["one"]) & FileFilter(__file__)
    mc = MemCache()
    stuff = []
    def one(a, b):
        c = a * b
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=c))
        return c

    def two(x, y, z):
        memo = x + 2 * y * z
        frame = sys._getframe(0)
        stuff.append(Call(frame=frame))
        stuff.append(Return(frame=frame, retval=memo))
        return memo

    sys.settrace(tracer(mc, f))
    one(1,2)
    two(1,2,3)
    sys.settrace(None)    

    assert stuff[0].id not in mc.cache

    assert mc.get_cache_for_func(stuff[2].id) == stuff[2:4]


def test_settrace_handler4():
    f = FunctionNameFilter(include=["two"], exclude=["one"]) & FileFilter(__file__)
    mc = MemCache()
    stuff = []
    def one(a, b):
        c = a * b
        frame = sys._getframe(0)
        stuff.append({
            'call': Call(frame=frame), 
            'return': Return(frame=frame, retval=c)})
        return c

    def two(x, y, z):
        memo = x + 2 * y * z
        frame = sys._getframe(0)
        stuff.append({
            'call': Call(frame=frame), 'return': Return(frame=frame, retval=memo)})
        return memo

    sys.settrace(stracer(mc, f))
    one(1,2)
    two(1,2,3)
    sys.settrace(None)    

    assert mc.get_cache_for_func(stuff[1]['call'].id) == [stuff[1]]