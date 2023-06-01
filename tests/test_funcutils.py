from callcache.funcutils import get_function_id
import sys, os

def test_get_function_id():
    frame = sys._getframe(0)
    file_name = frame.f_code.co_filename
    function_name = frame.f_code.co_name

    assert os.path.basename(file_name) == "test_funcutils.py"
    assert function_name == "test_get_function_id"
    file_id = get_function_id(file_name, function_name)

    assert file_id == "2be8c54da50deee225178de0ca4f3ce4"