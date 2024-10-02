def getWindowsCommandResult():
    import subprocess
    commands = ['powershell Get-NetRoute', 'powershell Get-NetIPAddress']

    for command in commands:
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            yield result
        except subprocess.CalledProcessError as e:
            print(f"Error executing command '{command}': {e}")
            return
