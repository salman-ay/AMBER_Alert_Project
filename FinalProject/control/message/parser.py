import re
from collections import namedtuple
from .exceptions import JobNotFound, ActionNotFound

Command = namedtuple('Command', ['job', 'action', 'parameter'])


def extract_part(message: str):
    parts = message.split(":")
    return parts


def get_job(jobs, name: str):
    _job = jobs.get(name)
    if not _job:
        raise JobNotFound(f"No job {name}")
    return _job


def get_action(_job, action_name: str):
    action = getattr(_job, action_name)
    if not _job:
        raise ActionNotFound(f"No action {action_name}")
    return action


def parse_command(message: str):
    lines = message.split("\n")
    commands = []
    for line in lines:
        parts = extract_part(line)
        if len(parts) != 3:
            continue
        command = Command(parts[0].strip(), parts[1].strip(), parts[2].strip())
        commands.append(command)
    return commands


def translate_command(jobs, command):
    job = get_job(jobs, command.job)
    action = get_action(job, command.action)
    parameter = command.parameter
    return job, action, parameter

