from .fastlane_pilot_output_log_error_checker import get_errors, print_errors
from python_pretty_print import pretty_print
from python_command_runner import *


def run_attempt(command: list[str], timeout_seconds: int, print_log_stream: bool = False) -> None:
	"""Raises exceptions on failure. No exception = success."""
	
	header = f"Showing {'all' if print_log_stream else 'filtered'} logs "
	print(f"\n{header:=<100}\n")

	success, lines = _run_attempt_command(command, timeout_seconds, print_log_stream)
	errors = get_errors(success, lines)

	if len(errors) > 0:
		if not print_log_stream:
			pretty_print(f"<error>\n{'Found errors! Showing all logs ':=<100}\n</error>")
			for line in lines:
				color = "error" if line.source == OutputSource.STDERR else "dull"
				pretty_print(f"[{line.index}]<{color}>[{line.source}]</{color}> {line.text}")

		if success:
			print()
			print("Something peculiar has happened. fastlane indicated success, but there seem to be errors.")

		print_errors(errors)


def _run_attempt_command(command: list[str], timeout_seconds: int, print_log_stream: bool = False) -> tuple[bool, list[OutputLine]]:
	""" returns (success, lines) """
	lines: list[OutputLine] = []
	generator = run_command(command, timeout_seconds=timeout_seconds)

	in_success_part = False

	try:
		while True:
			output_line = next(generator)
			lines.append(output_line)

			if "Successfully uploaded package to App Store Connect".lower() in output_line.text.lower():
				in_success_part = True

			if print_log_stream or _is_useful_status_log(output_line) or in_success_part:
				log = output_line.text
				if output_line.source == OutputSource.STDERR:
					log = "<error>[STDERR]</error> " + log
					pretty_print(log)

			if "Successfully distributed build to Internal testers".lower() in output_line.text.lower():
				in_success_part = False

	except StopIteration as exception:
		return (exception.value == 0, lines)


def _is_useful_status_log(line: OutputLine) -> bool:
	contains_checks = [
		"Ready to upload new build to TestFlight",
		"Going to upload updated app to App Store Connect",
		"Successfully uploaded the new binary to App Store Connect",
		"Waiting for the build to show up in the build list",
		"Successfully finished processing the build",
		"Successfully set the changelog for build",
	]
	for contains_check in contains_checks:
		if contains_check in line.text:
			return True

	return False
