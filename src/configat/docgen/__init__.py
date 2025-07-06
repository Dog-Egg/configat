from __future__ import annotations

import os
from typing import Any

import pathspec


def walk_python_files(base_dir: str):
    """遍历当前目录及子目录的所有 .py 文件，并排除 .gitignore 中定义的规则"""
    with open(".gitignore", "r") as f:
        spec = pathspec.PathSpec.from_lines("gitwildmatch", f)

    all_files = []
    for root, dirs, files in os.walk(base_dir or "."):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path.endswith(".py"):
                if spec.match_file(full_path):
                    continue
                all_files.append(full_path)
    return sorted(all_files)


def parse_code(code: str):
    """使用抽象语法树，获取 configat.resolve() 中的参数"""
    import ast

    results: list[tuple[str, Any]] = []

    for node in ast.walk(ast.parse(code)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
        ):
            if node.func.value.id == "configat" and node.func.attr == "resolve":
                args = node.args
                expr_value = None
                if len(args) >= 1 and isinstance(args[0], ast.Constant):
                    expr_value = args[0].value

                help_value = ""
                kwargs = node.keywords
                for kw in kwargs:
                    if kw.arg == "help":
                        if isinstance(kw.value, ast.Constant):
                            help_value = kw.value.value

                if isinstance(expr_value, str):
                    results.append((expr_value, help_value))
    return results
