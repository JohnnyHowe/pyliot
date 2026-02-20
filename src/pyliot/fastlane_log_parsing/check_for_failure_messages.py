import re
from typing import Callable, Iterable
from python_command_runner import OutputLine, OutputSource
from .exceptions import *


def error_checker(priority: int = 0):
    def decorator(func):
        func.priority = priority
        return func
    return decorator


class LogErrorChecker:

    # =============================================================================================
    # region Interface 
    # =============================================================================================

    def __init__(self, logs: list[OutputLine]) -> None:
        self.logs = logs

    def throw_exceptions_on_errors(self):
        for exception in self.get_exceptions():
            raise exception
            return  # for when some debuggers allow you to continue

    def get_exceptions(self) -> Iterable[Exception]:
        for method in self._get_exception_check_methods():
            try:
                method()
            except Exception as exception:
                yield exception

    # =============================================================================================
    # region Finding error check methods
    # =============================================================================================

    def _get_exception_check_methods(self) -> Iterable[Callable]:
        methods = list(self._get_unordered_exception_check_methods())
        return sorted(methods, key=lambda method: getattr(method, "priority", 0), reverse=True)

    def _get_unordered_exception_check_methods(self) -> Iterable[Callable]:
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if self._is_error_check_method(attribute):
                yield attribute 
        
    def _is_error_check_method(self, attribute) -> bool:
        if not callable(attribute):
            return False
        if getattr(attribute, "priority", None) is None:
            return False
        return True

    # =============================================================================================
    # region Error catching methods helpers
    # =============================================================================================

    def _get_stderr_text_lines(self) -> Iterable[str]:
        for line in self._get_stderr_lines():
            yield line.text

    def _get_stderr_lines(self) -> Iterable[OutputLine]:
        for line in self.logs:
            if line.source == OutputSource.STDERR:
                yield line

    # =============================================================================================
    # region Error catching methods
    # =============================================================================================

    @error_checker(priority=-1)
    def _generic_error_catcher(self):
        failure_patterns = [
            "error",
            "failure",
            "failed"
        ]

        for line in self._get_stderr_text_lines():
            for failure_pattern in failure_patterns:
                if not failure_pattern in line.lower():
                    continue
                raise UnknownUploadException(f"Found \"{failure_pattern}\" in line:\n{line}")

    @error_checker()
    def _check_duplicate_build_number_error(self):
        pattern = re.compile(r"\[altool\].*The bundle version must be higher than the previously uploaded version: [\"'‘’“”]?(\d)[\"'‘’“”]")
        for line in self._get_stderr_text_lines():
            match = pattern.search(line)
            if match:
                raise ValueError(f"The build number {match.group(1)} has already been used! The new build will not be available in App Store Connect.")


def check_for_failure_messages(logs: list[OutputLine]) -> None:
    """Raises exceptions on errors found."""
    LogErrorChecker(logs).throw_exceptions_on_errors()


e = LogErrorChecker([])
print("error check methods:")
for i in e._get_exception_check_methods():
    print("\t" + i.__name__)