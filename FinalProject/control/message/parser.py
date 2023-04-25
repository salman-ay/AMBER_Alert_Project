import re
from collections import namedtuple
from .exceptions import JobNotFound, ActionNotFound

Command = namedtuple('Command', ['job', 'action', 'parameter', 'type', 'color', 'license'])


def extract_part(message: str):
    return message.split(":")


def extract_vehicle_information(message: str):
    return message.split("-")


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
        if len(parts) != 4:
            continue
        vehicle_parts = extract_vehicle_information(parts[3].strip())
        command = Command(parts[0].strip(), parts[1].strip(), parts[2].strip(),
                         vehicle_parts[0].strip(), vehicle_parts[1].strip(), vehicle_parts[2].strip())
        commands.append(command)
    return commands


def translate_command(jobs, command):
    job = get_job(jobs, command.job)
    action = get_action(job, command.action)
    parameter = command.parameter
    info = [command.type, command.color, command.license]
    return job, action, parameter, info

