class Server:
    """
    A class used to represent a server.

    Attributes
    ----------

    users : list
        A list of connected users.

    Methods
    -------
    conn_user(new_users)
        Connect users to the server.

    disc_user(connected_user)
        Prints the animals name and what sound it makes
    """

    def __init__(self: object, users: list):
        """
        Parameters
        ----------
        users: list
            A list of connected users.
        """

        self.__users: list = users

    @property
    def users(self: object) -> list:
        return self.__users

    def conn_user(self: object, new_users: object) -> None:
        """Connect new users to the server.

        Parameters
        ----------
        new_users : object
            The user which will be connected.
        """

        all_users = self.__users
        for user in new_users:
            all_users.append(user)
        self.__users = all_users
        return None

    def disc_user(self: object, connected_user: object) -> None:
        """Disconnect users from the server.

        Parameters
        ----------
        connected_user : object
            The user which will be disconnected.
        """

        all_users = self.__users
        all_users.remove(connected_user)
        self.__users = all_users
        return None
