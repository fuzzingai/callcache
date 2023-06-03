from callcache.cache.mem import MemCache, BaseCache
from callcache.calltypes import Call, Return
import sys

def test_save_mem():
    a = MemCache()

    current_call = Call(sys._getframe(0))
    a.save(current_call)

    assert a.cache == {current_call.id: [current_call]}
    assert a.get_cache_for_func(current_call.id) == [current_call]

    def no(cache):
        new_call = Call(sys._getframe(0))
        cache.save(new_call)

        assert cache.cache == {current_call.id: [current_call], new_call.id: [new_call]}
        assert cache.get_cache_for_func(new_call.id) == [new_call]

    no(a)


def test_ssave_mem():
    a = MemCache()

    current_call = Call(sys._getframe(0))
    current_return = Return(sys._getframe(0), 1)

    unique_id = "abc"
    a.ssave(unique_id, current_call)
    a.ssave(unique_id, current_return)

    assert a.cache == {current_call.id: [(current_call, current_return)]}