
from analyzer.code_analyzer import check_code_quality


def test_quality_checker_detects_unused_import():
    code = "import os\n"

    result = check_code_quality(code)

    assert result["success"] is True
    assert any(
        issue["code"] == "F401"
        for issue in result["issues"]
    )


def test_quality_checker_accepts_clean_code():
    code = "print('Hello, world!')\n"

    result = check_code_quality(code)

    assert result["success"] is True
    assert result["issues"] == []
