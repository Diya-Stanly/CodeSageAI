
from analyzer.code_analyzer import analyze_code


def test_valid_python_code():
    result = analyze_code('print("Hello, world!")')

    assert result["valid"] is True
    assert result["line"] is None


def test_invalid_python_code():
    result = analyze_code("def greet(:\n    print('Hello')")

    assert result["valid"] is False
    assert result["line"] == 1


def test_empty_code_is_valid():
    result = analyze_code("")

    assert result["valid"] is True
