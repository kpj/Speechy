def get_available_commands():
    """ Return list of all command classes
    """
    import commands
    classes = [getattr(commands, x) for x in dir(commands) if isinstance(getattr(commands, x), type) and x != 'BaseCommand']
    return classes


if __name__ == '__main__':
    for Cmd in get_available_commands():
        print(Cmd().text)
