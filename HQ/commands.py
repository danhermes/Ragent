from HQ.tasks import (
    check_task_completion,
    advance_task_setup,
    show_task_status
)

def handle_command(command_str: str):
    tokens = command_str.strip().split()
    if not tokens:
        print("(Blane) > No command entered.")
        return

    verb = tokens[0]
    args = tokens[1:]

    if verb == "assign":
        advance_task_setup()
    elif verb == "status":
        return show_task_status()
    elif verb in ["answer", "set"]:
        if args:
            field, value = args[0], " ".join(args[1:])
            check_task_completion(field, value)
        else:
            print("(Blane) > Usage: set <field> <value>")
    else:
        print(f"(Blane) > Unknown command: {verb}")
