class User:
    """
    A class used to represent an user.

    Attributes
    ----------

    tick: int
        Informs when user was connected.

    ttask: int
        Informs for how many ticks the user may stay connected.
    """

    def __init__(self: object, tick: int, ttask: int):
        """
        Parameters
        ----------
        tick: int
            Informs when user was connected.

        ttask: int
            Informs for how many ticks the user may stay connected.
        """

        self.__tick: int = tick
        self.__ttask: int = ttask
        self.__tickout: int = self._generate_tickout

    @property
    def tickout(self: object) -> int:
        return self.__tickout

    @property
    def _generate_tickout(self: object) -> int:
        return self.__tick + self.__ttask
