def commands_parser(message):
    com = ["advanced", "male", "female", "off", "on", "primitive"]
    if len(message) >= 1:
        if message[0] == "/":
            pre_command = message[1:]
            command = pre_command.split(" ")
            if command[0] in com:
                return True, command[0]
            else:
                return True, "Invalid"
        else:
            return False, None
    else:
        return False, None