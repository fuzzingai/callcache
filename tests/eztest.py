import sys
from callcache.tracefilters import FunctionNameFilter, FileFilter
from callcache.cache.mem import MemCache
from callcache.callhooks import stracer
# create a filter function
f = FunctionNameFilter(include=["one", "three"], exclude=["two"])

# create a cache, there will be more types later
mc = MemCache()

# get your functions defined or whatever
def one(a, b):
    c = a * b
    return c

def two(x, y, z):
    memo = x + 2 * y * z
    return memo

def three():
    print("hi")
    return "beans"

sys.settrace(stracer(mc, f))
one(1,2)
two(1,2,3)
one(5, 9)
three()
sys.settrace(None)    

def gen_tests(cache):

    buf = ""

    for key, value in cache.items():
        print(value)
        for call, ret in value:

            args = ', '.join(f"{k}={v!r}" for k, v in call.args.items())
            buf += f"""
    def test_{call.function_name}():
        assert {call.function_name}({args}) == {ret.retval}\n"""

    return buf

print(gen_tests(mc.cache))