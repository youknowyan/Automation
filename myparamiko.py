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
        print('Now connection is closing')
        ssh_client.close()
        print('Now connection is closed')

### below is for test purpose
if __name__ == '__main__': 
      
    # routers info:
    router1 = {'server_IP':'10.1.6.10', 'server_PORT': '22', 'username': 'user1', 'password': 'Example123'}
    router2 = {'server_IP':'10.1.6.11', 'server_PORT': '22', 'username': 'user1', 'password': 'Example123'}
    router3 = {'server_IP':'10.1.6.12', 'server_PORT': '22', 'username': 'user1', 'password': 'Example123'}

    # Add more server to the list if needed.
    routers = [router1, router2, router3]

    # iterating all servers in the list and backup the config
    for router in routers:
        client = myparamiko.connect(**router)
        shell = myparamiko.open_shell(client)

        myparamiko.send_command(shell, 'terminal length 0')
        myparamiko.send_command(shell, 'enable')
        myparamiko.send_command(shell, 'Example123')  # this is the enable command
        myparamiko.send_command(shell, 'show run')

        output = myparamiko.show(shell)

        # process output
        output_list = output.splitlines()
        output_list = output_list[11:-1]
        output = '\n'.join(output_list)
        # name the backup file
        from datetime import datetime
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        file_name = f'{router["server_ip"]}_{year}-{month}-{day}.txt'
        print(file_name)

        # Backup the file
        with open(file_name, 'w') as f:
            f.write(output)

        myparamiko.close(client)



