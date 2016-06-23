from wutu_compiler.core.common import create_stream, add_variable, get_data


def test_string_argument():
    stream = create_stream()
    add_variable(stream, "test", "hello")
    result = get_data(stream).strip()
    excepted = "var test = \"hello\";"
    assert excepted == result


def test_int_argument():
    stream = create_stream()
    add_variable(stream, "test", 123)
    result = get_data(stream).strip()
    excepted = "var test = 123;"
    assert excepted == result
