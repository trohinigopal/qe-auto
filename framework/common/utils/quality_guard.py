from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


def _python_files(project_root: Path) -> list[Path]:
    return [p for p in project_root.rglob("*.py") if ".venv" not in p.parts]


def _detect_duplicate_bdd_steps(project_root: Path) -> dict[str, list[str]]:
    occurrences: dict[str, list[str]] = {}
    for py_file in _python_files(project_root):
        source = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", "") in {"given", "when", "then"}:
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    step = node.args[0].value.strip()
                    occurrences.setdefault(step, []).append(str(py_file))
    return {k: v for k, v in occurrences.items() if len(v) > 1}


def run_quality_checks(project_root: Path) -> None:
    print("Running lint and quality checks...")
    subprocess.call([sys.executable, "-m", "pytest", "--collect-only"], cwd=project_root)
    subprocess.call([sys.executable, "-m", "compileall", "."], cwd=project_root)

    duplicates = _detect_duplicate_bdd_steps(project_root)
    if duplicates:
        print("Duplicate step definitions detected:")
        for step, files in duplicates.items():
            print(f"  STEP: {step}")
            for file in files:
                print(f"    - {file}")
    else:
        print("No duplicate BDD step definitions found.")
