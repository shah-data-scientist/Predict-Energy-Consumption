"""
FILE: mirror_modify_check.py
STATUS: Active
RESPONSIBILITY: Pre-commit hook enforcing 1-to-1 mapping between src/ and tests/ changes
LAST MAJOR UPDATE: 2026-02-10
MAINTAINER: Shahu
"""

import subprocess
import sys
from pathlib import PurePosixPath


def get_staged_files() -> list[str]:
    """Get list of staged Python files."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True,
    )
    return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]


def get_expected_test_path(src_path: str) -> str:
    """Map src/ file to expected tests/ file.

    Examples:
        src/services/chat.py -> tests/services/test_chat.py
        src/pipeline/reddit_chunker.py -> tests/pipeline/test_reddit_chunker.py
        src/core/config.py -> tests/core/test_config.py
    """
    p = PurePosixPath(src_path)
    # Remove "src/" prefix -> relative path
    relative = PurePosixPath(*p.parts[1:])
    # Build test path: tests/<subdir>/test_<filename>.py
    test_dir = PurePosixPath("tests", *relative.parent.parts)
    test_name = f"test_{relative.name}"
    return str(test_dir / test_name)


def get_flat_test_path(src_path: str) -> str:
    """Map src/ file to flat tests/ file (legacy layout).

    Examples:
        src/services/chat.py -> tests/test_chat.py
        src/pipeline/reddit_chunker.py -> tests/test_reddit_chunker.py
    """
    p = PurePosixPath(src_path)
    filename = p.name
    return f"tests/test_{filename}"


def main() -> int:
    """Check that staged src/ files have corresponding test file changes."""
    staged = get_staged_files()

    src_files = [
        f for f in staged
        if f.startswith("src/")
        and f.endswith(".py")
        and "__init__" not in f
    ]

    if not src_files:
        return 0

    missing = []
    for src_file in src_files:
        expected_mirror = get_expected_test_path(src_file)
        expected_flat = get_flat_test_path(src_file)

        # Accept either mirror structure or flat structure
        if expected_mirror not in staged and expected_flat not in staged:
            # Also check with backslashes (Windows)
            mirror_win = expected_mirror.replace("/", "\\")
            flat_win = expected_flat.replace("/", "\\")
            if mirror_win not in staged and flat_win not in staged:
                missing.append((src_file, expected_mirror, expected_flat))

    if missing:
        print("\nMirror & Modify Policy Violation:")
        for src, mirror, flat in missing:
            print(f"  Modified '{src}' but neither '{mirror}' nor '{flat}' is staged.")
        print()
        print("Commit Rejected.")
        print("Please update the corresponding test file and 'git add' it.")
        print("If this is a refactor/doc change, use '--no-verify' to bypass.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
