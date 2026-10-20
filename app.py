import difflib
from flask import Flask, render_template, request, jsonify

from analyzer.code_analyzer import (
    analyze_code,
    check_code_quality,
    fix_code,
)

app = Flask(__name__)

MAX_CODE_LENGTH = 50_000


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    source_code = data.get("code", "")

    if not isinstance(source_code, str):
        return jsonify({"error": "Code must be text."}), 400

    if len(source_code) > MAX_CODE_LENGTH:
        return jsonify({"error": "Code is too long. Maximum: 50,000 characters."}), 413

    syntax_result = analyze_code(source_code)

    if not syntax_result["valid"]:
        return jsonify({
            "syntax": syntax_result,
            "quality": None,
        })

    quality_result = check_code_quality(source_code)

    return jsonify({
        "syntax": syntax_result,
        "quality": quality_result,
    })


@app.route("/api/fix", methods=["POST"])
def auto_fix():
    data = request.get_json(silent=True) or {}
    source_code = data.get("code", "")

    if not isinstance(source_code, str):
        return jsonify({"error": "Code must be text."}), 400

    if len(source_code) > MAX_CODE_LENGTH:
        return jsonify({"error": "Code is too long. Maximum: 50,000 characters."}), 413

    syntax_result = analyze_code(source_code)

    if not syntax_result["valid"]:
        return jsonify({
            "error": "Fix syntax errors before using the auto-fixer."
        }), 400

    
    result = fix_code(source_code)

    if not result["success"]:
        return jsonify(result), 500

    original_lines = source_code.splitlines()
    fixed_lines = result["fixed_code"].splitlines()

    matcher = difflib.SequenceMatcher(
        a=original_lines,
        b=fixed_lines,
        autojunk=False,
    )

    diff_rows = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_lines = original_lines[i1:i2]
        new_lines = fixed_lines[j1:j2]

        if tag == "equal":
            for old, new in zip(old_lines, new_lines):
                diff_rows.append({
                    "type": "same",
                    "original": old,
                    "fixed": new,
                })

        elif tag == "delete":
            for old in old_lines:
                diff_rows.append({
                    "type": "removed",
                    "original": old,
                    "fixed": "",
                })

        elif tag == "insert":
            for new in new_lines:
                diff_rows.append({
                    "type": "added",
                    "original": "",
                    "fixed": new,
                })

        elif tag == "replace":
            paired_count = min(len(old_lines), len(new_lines))

            for index in range(paired_count):
                diff_rows.append({
                    "type": "changed",
                    "original": old_lines[index],
                    "fixed": new_lines[index],
                })

            for old in old_lines[paired_count:]:
                diff_rows.append({
                    "type": "removed",
                    "original": old,
                    "fixed": "",
                })

            for new in new_lines[paired_count:]:
                diff_rows.append({
                    "type": "added",
                    "original": "",
                    "fixed": new,
                })

    result["original_code"] = source_code
    result["diff_rows"] = diff_rows

    return jsonify(result), 200



if __name__ == "__main__":
    app.run(debug=True)

