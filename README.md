simple usage:

```python
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

```

now you can inspect the historical call/return values to each of the functions

```python
In [6]: import pprint; pprint.pprint(mc.cache)
{('<ipython-input-1-bdeb3841d0ae>', 'one'): [Call(filepath=<ipython-input-1-bdeb3841d0ae>, function=one, args={'a': 1, 'b': 2}),
                                             Return(filepath=<ipython-input-1-bdeb3841d0ae>, function=one, retval=2),
                                             Call(filepath=<ipython-input-1-bdeb3841d0ae>, function=one, args={'a': 5, 'b': 9}),
                                             Return(filepath=<ipython-input-1-bdeb3841d0ae>, function=one, retval=45)],
 ('<ipython-input-1-bdeb3841d0ae>', 'three'): [Call(filepath=<ipython-input-1-bdeb3841d0ae>, function=three, args={}),
                                               Return(filepath=<ipython-input-1-bdeb3841d0ae>, function=three, retval=beans)]}
```