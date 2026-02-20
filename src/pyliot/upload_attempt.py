from python_pretty_print import pretty_print
from python_command_runner import OutputSource, OutputLine, run_command

from .fastlane_log_parsing.check_for_success_messages import check_for_success_messages


def run_attempt(command: list[str], timeout_seconds: int) -> None:
	"""Raises exceptions on failure. No exception = success."""
	
	exit_code, lines = _run_attempt_command(command, timeout_seconds)

	if exit_code == 0:
		check_for_success_messages(lines)
	else:
		raise RuntimeError(f"Upload command failed with exit code {exit_code}.")


def _run_attempt_command(command: list[str], timeout_seconds: int) -> tuple[int, list[OutputLine]]:
	""" returns (exit_code, lines) """
	lines: list[OutputLine] = []
	generator = run_command(command, timeout_seconds=timeout_seconds)

	try:
		while True:
			output_line = next(generator)
			lines.append(output_line)
			log = output_line.text
			if output_line.source == OutputSource.STDERR:
				log = "<error>[STDERR]</error> " + log
				pretty_print(log)


	except StopIteration as exception:
		return (exception.value, lines)
