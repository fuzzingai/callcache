from callcache.cache.mem import MemCache, BaseCache
from callcache.calltypes import Call, Return, _serialize_frame
import sys, tempfile, pickle, dill
from IPython import embed

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


def test_buffered_call_return_save_mem():
    a = MemCache()

    current_call = Call(sys._getframe(0))
    current_return = Return(sys._getframe(0), 1)

    unique_id = "abc"
    a.buffered_call_return_save(unique_id, current_call)
    a.buffered_call_return_save(unique_id, current_return)

    assert a.cache == {current_call.id: [{
        'call': current_call, 
        'return': current_return}]}

def test_memcache_save_to_file():
    a = MemCache()

    current_call = Call(sys._getframe(0))
    current_return = Return(sys._getframe(0), 1)

    unique_id = "abc"
    a.buffered_call_return_save(unique_id, current_call)
    a.buffered_call_return_save(unique_id, current_return)

    assert a.cache == {current_call.id: [{
        'call': current_call, 
        'return': current_return}]}

    with tempfile.NamedTemporaryFile() as f:
        # get the temp filename
        filename = f.name

        a.save_to_file(filename)

        #now parse the tempfile
        restored_cache = pickle.load(open(filename, 'rb'))

        cached_call = restored_cache.cache[current_call.id][0]['call']
        cached_return = restored_cache.cache[current_call.id][0]['return']

        assert cached_call.filepath == current_call.filepath
        assert cached_call.function_name == current_call.function_name
        assert cached_call.args == current_call.args

        assert cached_return.filepath == current_return.filepath
        assert cached_return.function_name == current_return.function_name
        assert cached_return.retval == current_return.retval