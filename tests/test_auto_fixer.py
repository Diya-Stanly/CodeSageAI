
from analyzer.code_analyzer import fix_code


def test_auto_fixer_removes_unused_import():
    code = "import os\n\nprint('Hello')\n"

    result = fix_code(code)

    assert result["success"] is True
    assert "import os" not in result["fixed_code"]
    assert "print('Hello')" in result["fixed_code"]
