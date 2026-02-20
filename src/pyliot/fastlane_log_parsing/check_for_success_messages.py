import re
from python_command_runner import OutputLine
from .exceptions import UnknownUploadException

REQUIRED_PATTERNS = [
    "Successfully uploaded package to App Store Connect",
    "Successfully finished processing the build",
]

def check_for_success_messages(logs: list[OutputLine]) -> None:
    """Raises exceptions on errors found."""
    for pattern in REQUIRED_PATTERNS:
        if _pattern_exists_in_logs(logs, pattern):
            continue
        raise UnknownUploadException(f'Could not find pattern "{pattern}" in logs! Treating as failure.')


def _pattern_exists_in_logs(logs: list[OutputLine], pattern: str) -> bool:
    pattern_compiled = re.compile(pattern)
    for line in logs:
        if pattern_compiled.search(line.text):
            return True
    return False
