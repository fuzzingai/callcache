from callcache.tracefilters import FileFilter, FunctionNameFilter, AndFilter, OrFilter
import sys

def test_filefilter():
    f = FileFilter(__file__)

    assert f.keep_frame(sys._getframe(0)) == True 

def test_filters1():
    f = FileFilter(__file__)

    assert f.keep_frame(sys._getframe(0)) == True

    def a():
        assert f.keep_frame(sys._getframe(0)) == True 

    a()

def test_function_name_filter():
    f = FunctionNameFilter("test_function_name_filter")
    b = FunctionNameFilter("a")

    assert f.keep_frame(sys._getframe(0)) == True 
    assert b.keep_frame(sys._getframe(0)) == False 

    def a():
        assert f.keep_frame(sys._getframe(0)) == False
        assert b.keep_frame(sys._getframe(0)) == True 

    a()

def test_filters2():
    f = FileFilter(__file__) & FunctionNameFilter("test_filters2")
    b = FileFilter(__file__) & FunctionNameFilter("a")
    
    def a():
        assert f.keep_frame(sys._getframe(0)) == False
        assert b.keep_frame(sys._getframe(0)) == True 

    assert f.keep_frame(sys._getframe(0)) == True
    assert b.keep_frame(sys._getframe(0)) == False

    a()


def test_filters3():
    a = FunctionNameFilter("a") 
    b = FunctionNameFilter("test_filters3")
    frame = sys._getframe(0)

    c = a & b
    d = a | b

    assert c != a
    assert c != b
    assert c == AndFilter(a, b)
    assert c.keep_frame(frame) == False 

    assert d != a
    assert d != b
    assert d == OrFilter(a, b)
    assert d.keep_frame(frame) == True 

def test_filters4():
    a = FunctionNameFilter(include=["c", "test_filters4"])
    assert a.keep_frame(sys._getframe(0)) == True

    def b():
        assert a.keep_frame(sys._getframe(0)) == False
    def c():
        assert a.keep_frame(sys._getframe(0)) == True

    b()
    c()

    a = FunctionNameFilter("c") | FunctionNameFilter("test_filters4")
    b()
    c()

    a = FunctionNameFilter(exclude=["a", "test_filters4"])
    assert a.keep_frame(sys._getframe(0)) == False

    # the include filter is looked at before the exclude ones. i could make this a set but idc
    a = FunctionNameFilter(include=["test_filters4"], exclude=["test_filters4"])
    assert a.keep_frame(sys._getframe(0)) == True 

