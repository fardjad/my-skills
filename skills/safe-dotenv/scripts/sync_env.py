#!/usr/bin/env python3
"""Synchronize a local .env file from its adjacent authoritative .env.example."""

from __future__ import annotations

import argparse
import os
import re
import stat
import tempfile
from pathlib import Path


ASSIGNMENT = re.compile(r"^(\s*(?:export\s+)?)([A-Za-z_][A-Za-z0-9_]*)(\s*=\s*)(.*?)(\r?\n)?$")
UNASSIGNED = re.compile(r"^\s*(?:export\s+)?[A-Za-z_][A-Za-z0-9_]*\s*(?:#[^\r\n]*)?(?:\r?\n)?$")


def _assignment_parts(line: str, path: Path, line_number: int) -> tuple[str, str, str, str] | None:
    """Return assignment prefix, value, and newline, or None for comments/blanks."""
    match = ASSIGNMENT.fullmatch(line)
    if match:
        return match.group(1) + match.group(2), match.group(4), match.group(5) or "", match.group(3)
    if not line.strip() or line.lstrip().startswith("#"):
        return None
    raise ValueError(f"Unsupported dotenv syntax in {path} at line {line_number}")


def _split_inline_comment(value: str) -> tuple[str, str]:
    """Separate a trailing unquoted comment while keeping # inside values intact."""
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "#" and index > 0 and value[index - 1].isspace():
            return value[:index].rstrip(), value[index - 1 :]
    return value.rstrip(), ""


def _read_assignments(path: Path) -> dict[str, str]:
    """Read only assignment values needed for synchronization; never print them."""
    assignments: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError:
        raise ValueError(f"Invalid UTF-8 in {path}") from None
    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        # A bare key is unset in dotenv, so retain the template's default instead.
        if UNASSIGNED.fullmatch(line):
            continue
        parts = _assignment_parts(line, path, line_number)
        if parts is None:
            continue
        name_prefix, raw_value, _newline, _assignment_separator = parts
        name_match = re.search(r"[A-Za-z_][A-Za-z0-9_]*$", name_prefix)
        assert name_match is not None
        name = name_match.group(0)
        value, _comment = _split_inline_comment(raw_value)
        if name in assignments:
            raise ValueError(f"Duplicate variable in {path} at line {line_number}")
        assignments[name] = value
    return assignments


def _paired_example(path: Path) -> Path:
    if not path.name.startswith(".env"):
        raise ValueError("file name must start with .env")
    if path.name.endswith(".example"):
        return path
    return path.with_name(f"{path.name}.example")


def sync(example_path: Path) -> Path:
    """Apply example ordering/comments and variables, preserving existing values."""
    example_path = example_path.resolve()
    env_path = example_path.with_name(example_path.name[: -len(".example")])
    template_text = example_path.read_text(encoding="utf-8")
    existing = _read_assignments(env_path) if env_path.exists() else {}

    output: list[str] = []
    seen: set[str] = set()
    for line_number, line in enumerate(template_text.splitlines(keepends=True), start=1):
        parts = _assignment_parts(line, example_path, line_number)
        if parts is None:
            output.append(line)
            continue
        name_prefix, template_value_with_comment, newline, assignment_separator = parts
        name_match = re.search(r"[A-Za-z_][A-Za-z0-9_]*$", name_prefix)
        assert name_match is not None
        name = name_match.group(0)
        if name in seen:
            raise ValueError(f"Duplicate variable {name} in {example_path} at line {line_number}")
        seen.add(name)
        template_value, template_comment = _split_inline_comment(template_value_with_comment)
        value = existing.get(name, template_value)
        suffix = f" {template_comment.lstrip()}" if template_comment else ""
        output.append(f"{name_prefix}{assignment_separator}{value}{suffix}{newline}")

    # For a new local file, do not make credentials world-readable.
    mode = stat.S_IMODE(env_path.stat().st_mode) if env_path.exists() else 0o600
    fd, temporary_name = tempfile.mkstemp(prefix=".env.", dir=env_path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as temporary:
            temporary.write("".join(output))
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, env_path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return env_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="path to a dotenv file or its adjacent .example template")
    args = parser.parse_args()
    try:
        example_path = _paired_example(args.file)
    except ValueError as error:
        parser.error(str(error))
    if not example_path.is_file():
        parser.error(f"missing adjacent example file: {example_path}")
    env_path = sync(example_path)
    print(f"Synchronized {env_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
