from time import sleep
from typing import List

from models.servers import Server
from models.users import User

servers_in_use: List[Server] = []


def main() -> None:

    print("Save the input file data as 'input.txt' in the folder where the 'main.py' is saved.")
    leave = input("If you want to proceed, please enter 'Yes'.\n").title()

    if leave != 'Yes':
        exit(0)

    users_per_tick, ttask, umax = read_file()  # Read file info and verifies if ttask and umax are within the range.

    tick = 1  # Start ticking.
    servers_in_use = []
    users_per_server_per_tick = []  # No user.
    cost_for_tick = 0

    jump_flag = len(users_per_tick)  # To avoid unnecessary code execution.

    while tick != 0:

        disconnect_user(tick, servers_in_use)  # Disconnect users and release servers.
        servers_in_use = release_server(servers_in_use)

        if tick <= jump_flag:  # After the whole input data is treated, skip some code execution.

            list_of_users = []

            if users_per_tick[tick - 1] != 0:  # Users must be connected to the servers.
                for i in range(users_per_tick[tick - 1]):  # Create list of users
                    user: User = User(tick, ttask)
                    list_of_users.append(user)

                if len(servers_in_use) != 0:
                    remainder_users = check_if_available(servers_in_use, umax, list_of_users)
                    if remainder_users:
                        servers_in_use = create_server(list_of_users, umax)
                else:
                    servers_in_use = create_server(list_of_users, umax)

        cost_for_tick += (len(servers_in_use) * 1)  # Pay for each running server at every tick.

        if len(servers_in_use):  # Count the connected users if server is running.
            connected_users = count_users_connected(servers_in_use)  # List of users connected to servers at every tick.
        else:  # Last server was released.
            connected_users = [0]  # Print 0 to indicate no user connected.

        users_per_server_per_tick.append(connected_users)  # Collect the data for future output.

        if len(servers_in_use) != 0:  # Servers still in use. Keep until all are released.
            tick += 1
        else:  # All servers released. Prepare output file.
            users_per_server_per_tick.append(cost_for_tick)   # Append the cost for tick.
            write_output_file(users_per_server_per_tick)  # Write to file.
            tick = 0  # Reset tick to leave.

    print('Output file is available.')
    sleep(5)
    exit(0)


def create_server(list_of_users, umax):
    """Create one or more servers to the users.

    Parameters
    ----------
    list_of_users : list
        List of users that will be connected to the server.

    umax : int
        Indicates the maximum allowed number of connected users.
    """

    if len(list_of_users) <= umax:  # If users <= umax
        server: Server = Server(list_of_users)  # Create server with users
        servers_in_use.append(server)
    else:
        for i in range(int(len(list_of_users) / umax) + 1):  # (len(list_of_users)/umax) sets plus one for the remainders.
            partial_users = list_of_users[:umax]
            server: Server = Server(partial_users)  # Create server with users
            servers_in_use.append(server)
            del (list_of_users[:umax])
    return servers_in_use


def check_if_available(servers_in_use, umax, list_of_users):
    """Checck if there are servers with less than maximum allowed number of users.

    The latest created servers are check first and used so that the older ones
    have more chance of being released.

    Parameters
    ----------
    servers_in_use : list
        List of created servers.

    umax : int
        Indicates the maximum allowed number of connected users.

    list_of_users : list
        List of users that will be connected to the server.
    """

    for server in reversed(servers_in_use):  # Check first if the latest created servers are available.
        users_conn = len(server.users)  # Load number of users connected to the server
        if users_conn < umax:  # If possible, connect users.
            slicer = umax - users_conn  # The list of users will decrease.
            partial_list = list_of_users[:slicer]  # Create a list with users that can be connected to the server.
            server.conn_user(partial_list)  # Connect the user to the server.
            del(list_of_users[:slicer])  # Remove the users that can be connected to the server.
    return len(list_of_users)


def disconnect_user(clock, used_servers):
    """Disconnect the user from the server.

    Check if the maximum amount of ticks allowed for the user was reached.

    Parameters
    ----------
    clock : list
        Current tick that will be compared with the timeout tick of the user.

    used_servers : list
        List of created servers that are working.
    """

    for server in used_servers:  # Check each server
        users_in_server = server.users  # Load all users connected to the server
        users_to_be_disconnected = []  # Create a list to be populated with the users that will be disconnected.
        for user in users_in_server:  # Check each user
            if user.tickout == clock:  # Time to disconnect
                users_to_be_disconnected.append(user)
        for user in users_to_be_disconnected:
            server.disc_user(user)  # Disconnect the users.
    return None


def release_server(working_servers):
    """Release the server if no user is connected to it.

    Parameters
    ----------
    working_servers : list
        List with all working servers.
    """

    to_be_removed = []
    for server in working_servers:  # Check each working server
        active_users = server.users  # Load all users connected to the server
        if len(active_users) == 0:  # No user connected.
            to_be_removed.append(server)
    for server in to_be_removed:
        if server in working_servers:  # Release the server if no user is connected to it.
            working_servers.remove(server)
    return working_servers


def count_users_connected(working_servers):
    """Count the number of users connected to the server at each tick.

    The information will be used in the output file.

    Parameters
    ----------
    working_servers : list
        List with all working servers.
    """

    users_in_servers = []
    for server in working_servers:  # Check each working server
        active_users = server.users  # Load all users connected to the server
        users_in_servers.append(len(active_users))  # Evaluates the number of users per server per tick.
    return users_in_servers


def read_file():
    """Read the input file."""

    with open('input.txt') as file:
        input_file = file.readlines()

    try:
        input_file = list(map(int, input_file))  # Turn data into to integers.
    except (ValueError, TypeError) as err:
        print(f'The data in the file is corrupted: {err}')
        print('Exiting.')
        sleep(5)
        exit(0)

    read_ttask = 0
    read_umax = 0
    users_in_each_tick = []  # Amount of users that are added by tick.

    for i in range(len(input_file)):
        if i == 0:
            read_ttask = input_file[i]
        elif i == 1:
            read_umax = input_file[i]
        else:
            users_in_each_tick.append(input_file[i])

    if (1 > read_ttask or read_ttask > 10) or (1 > read_umax or read_umax > 10):  # or 1 > umax > 10:
        print('The input file has invalid data or is empty.\n'
              'Please, correct the data or input another file.')
        print('Exiting.')
        sleep(5)
        exit(0)
    return users_in_each_tick, read_ttask, read_umax


def write_output_file(users_in_server):
    """Create the output file..

    Parameters
    ----------
    users_in_server : list
        Users that  were connected to each server at each tick.
    """

    with open('output.txt', 'a') as file:
        for elem in users_in_server:
            new_elem = str(elem).strip('[]')
            file.write(new_elem + '\n')


if __name__ == '__main__':
    main()
