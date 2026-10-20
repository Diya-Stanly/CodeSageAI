
# CodeSage AI 🛠️

A Python code analysis and auto-fixing dashboard that helps developers identify syntax errors, detect code-quality issues, and apply automatic fixes.

## ✨ Features

- **Syntax Analysis:** Detects Python syntax errors and reports the relevant line number.
- **Code Quality Checking:** Uses Ruff to identify code-quality issues.
- **Automatic Code Fixing:** Applies supported automatic fixes to Python code.
- **Code Comparison:** Displays the original and corrected code with highlighted changes.
- **Interactive Dashboard:** Provides a simple web interface for analyzing and fixing code.
- **Automated Testing:** Includes tests using pytest.

## 🧰 Tech Stack

- Python
- Flask
- Ruff
- pytest
- HTML
- CSS
- JavaScript

## 📁 Project Structure

```text
CodeSageAI/
├── analyzer/
│   └── code_analyzer.py
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   ├── test_code_analyzer.py
│   ├── test_code_quality.py
│   └── test_auto_fixer.py
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CodeSageAI.git
cd CodeSageAI
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository name if needed.

### 2. Create a virtual environment

```bash
py -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## 🧪 Running Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

## 🎯 Project Goal

CodeSage AI was built to explore Python static analysis, automated code correction, web application development, and software testing in a beginner-friendly project.

## 🔮 Future Improvements

- Support for additional code-quality checks.
- More detailed explanations of detected issues.
- Improved code comparison and error reporting.
- Additional automated tests and edge-case handling.

## 👩‍💻 Author

**Diya Stanly**

GitHub: https://github.com/Diya-Stanly
