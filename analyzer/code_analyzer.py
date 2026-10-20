
import ast


def analyze_code(source_code):
    """Check Python source code for syntax errors."""
    try:
        ast.parse(source_code)
        return {
            "valid": True,
            "message": "No syntax errors found!",
            "line": None,
        }
    except SyntaxError as error:
        return {
            "valid": False,
            "message": error.msg,
            "line": error.lineno,
        }

import subprocess
import sys
import tempfile
from pathlib import Path


def check_code_quality(source_code):
    """Check Python code for common quality issues."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        encoding="utf-8",
        delete=False,
    ) as temp_file:
        temp_file.write(source_code)
        file_path = Path(temp_file.name)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--output-format",
                "json",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode not in (0, 1):
            return {"success": False, "issues": [], "message": result.stderr}

        import json

        issues = json.loads(result.stdout)

        return {
            "success": True,
            "issues": [
                {
                    "code": issue["code"],
                    "message": issue["message"],
                    "line": issue["location"]["row"],
                }
                for issue in issues
            ],
            "message": f"Found {len(issues)} issue(s).",
        }
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        return {
            "success": False,
            "issues": [],
            "message": str(error),
        }
    finally:
        file_path.unlink(missing_ok=True)

def fix_code(source_code):
    """Apply safe automatic fixes supported by Ruff."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        encoding="utf-8",
        delete=False,
    ) as temp_file:
        temp_file.write(source_code)
        file_path = Path(temp_file.name)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--fix",
                "--output-format",
                "json",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode not in (0, 1):
            return {
                "success": False,
                "fixed_code": source_code,
                "message": result.stderr,
            }

        fixed_code = file_path.read_text(encoding="utf-8")

        return {
            "success": True,
            "fixed_code": fixed_code,
            "message": "Automatic fixes applied where possible.",
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "fixed_code": source_code,
            "message": "The fixer timed out.",
        }

    finally:
        file_path.unlink(missing_ok=True)
