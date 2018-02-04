import paramiko
from pprint import pprint

ip_address = '10.91.86.244'
username = 'admin'
password = 'A!min567'

print('--- Attempting connection to {}'.format(ip_address))

ssh_client = paramiko.SSHClient()

# Must set missing host key policy since we don't have the SSH key
# stored in the 'known_hosts' file
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Make the connection to our host.
ssh_client.connect(hostname=ip_address,
                   username=username,
                   password=password)

# If there is an issue, paramiko will throw an exception,
# so the SSH request must have succeeded.

print('--- Success! connected to: {} '.format(ip_address))
print('------------------------------------------------------\n')

# Execute some commands
stdin, stdout, stderr = ssh_client.exec_command('show ip route')
ip_route_table = stdout.readlines()
routes = [line.strip('\n') for line in ip_route_table]
for r in routes:
    print(r)

ssh_client.close()