import re

from python_command_runner import OutputLine

REQUIRED_PATTERNS = [
    "Successfully uploaded package to App Store Connect",
    "Successfully finished processing the build",
]

def check_for_success_messages(logs: list[OutputLine]) -> None:
    """ Raises exceptions on errors found. """
    for pattern in REQUIRED_PATTERNS:
        pattern_compiled = re.compile(pattern)
        
        for line in logs:
            if not pattern_compiled.search(line.text):
                raise Exception(f"Could not find pattern \"{pattern}\" in logs! Treating as failure.")