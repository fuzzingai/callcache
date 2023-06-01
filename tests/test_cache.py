from callcache.cache.mem import MemCache, BaseCache
from callcache.calltypes import Call, Return
import sys

def test_base_extension():
    extended_family = [MemCache, BaseCache]
    call = Call(sys._getframe(0))

    for cls in extended_family:
        a = cls()
        does_mapping_exist = a.ensure_id_mapping(call)
        assert does_mapping_exist == False
        assert a.func_id_map[call.id] == (call.filepath, call.function_name)
        del a


def test_base_cache_id_map():
    a = BaseCache()

    call1 = Call(sys._getframe(0))

    a.ensure_id_mapping(call1)

    assert a.id_map[call1.id] == (call1.filepath, call1.function_name)

    def b():
        call2 = Call(sys._getframe(0))
        a.ensure_id_mapping(call2)
        assert a.id_map[call1.id] == (call1.filepath, call1.function_name)
        assert a.id_map[call2.id] == (call2.filepath, call2.function_name)

    b()

def test_save_mem():
    a = MemCache()

    current_call = Call(sys._getframe(0))
    a.save(current_call)

    assert a.get_full_cache() == {current_call.id: [current_call]}
    assert a.get_cache_for_func(current_call.id) == [current_call]

    def no(cache):
        new_call = Call(sys._getframe(0))
        cache.save(new_call)

        assert cache.get_full_cache() == {current_call.id: [current_call], new_call.id: [new_call]}
        assert cache.get_cache_for_func(new_call.id) == [new_call]

    no(a)
