import subprocess
from config import REMOTE_HOST_1, REMOTE_USER_1, SSH_KEY_PATH_1
from config import REMOTE_HOST_2, REMOTE_USER_2, SSH_KEY_PATH_2

# Define the commands to execute on the remote servers
command_to_run = 'systemctl start jira  && echo "jira has started"'

try:
    # Use subprocess to open an SSH connection and run the command on the first host
    ssh_command_1 = f'ssh -i {SSH_KEY_PATH_1} {REMOTE_USER_1}@{REMOTE_HOST_1} "{command_to_run}"'
    subprocess.run(ssh_command_1, shell=True, check=True)

    # Use subprocess to open an SSH connection and run the command on the second host
    ssh_command_2 = f'ssh -i {SSH_KEY_PATH_2} {REMOTE_USER_2}@{REMOTE_HOST_2} "{command_to_run}"'
    subprocess.run(ssh_command_2, shell=True, check=True)

    print("Commands executed successfully on both hosts.")

except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
