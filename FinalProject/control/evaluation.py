from .message.parser import parse_command, translate_command


def execute(jobs, command):
    status = "OK"
    try:
        job, action, parameter = translate_command(jobs, command)
        result = action(parameter)
    except Exception as e:
        status = "ER"
        result = str(e)
    result = f"{status}:{result}"
    return result


def evaluate(jobs, message):
    commands = parse_command(message)
    results = []
    for command in commands:
        result = execute(jobs, command)
        results.append(result)
    return results
