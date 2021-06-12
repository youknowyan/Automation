import paramiko
import time

# To ssh connect a server
def connect(server_IP, server_Port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())     # To disregard Missing Host Key warning
    print(f'Now connecting to server {server_IP}')                       # Display which device is connecting
    ssh_client.connect(hostname=server_IP, port=server_Port, username=username, password=password,
                       look_for_keys=False, allow_agent=False)           # Connect
    return ssh_client

# Open Shell for input purpose
def open_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

# Type in command in shell
def send_command(shell, command, timout=1):
    print(f'Now sending command to server: {command}')
    shell.send(command + '\n')     # '\n' to execute command
    time.sleep(timout)

# Show what is displaying on shell
def show(shell, n=5000):
    output = shell.recv(n)
    return output.decode()

# Close ssh client
def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:   # Check if ssh client is still live
        print('Closing connection')
        ssh_client.close()

### below is for test purpose
if __name__ == '__main__':
    router_1 = {'server_IP': '10.1.6.20', 'server_PORT': '22', 'username':'user1', 'password':'Example123456'}
    New_client = connect(**router_1)
    shell = open_shell(New_client)

    send_command(shell, 'enable')
    send_command(shell, '123') # this is the enable password
    send_command(shell, 'term len 0')
    send_command(shell, 'show version')
    send_command(shell, 'show ip int brief')

    output = show(shell)
    print(output)



