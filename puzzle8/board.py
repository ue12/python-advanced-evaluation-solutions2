"""
This module implements the Board and State classes.
"""

from typing import Tuple, Generator
from math import sqrt

class Board:
    """
    Board class
    """

    __slots__ = ('values', 'size')

    def __init__(self, values: Tuple[int]):
        """Board constructor

        Args:
            values (Tuple[int]): values of the board.
        """
        self.size = round(sqrt(len(values)))
        self.values = values

    def __repr__(self):
        """__repr__ overload

        Returns:
            str: nice formatting of the Board.
        """
        line = lambda i: ' '.join(str(n) for n in self.values[self.size*i:self.size*(i+1)])
        res = '\n'.join(line(i) for i in range(self.size))
        return res.replace('0', '-')

    @property
    def nb_inv(self) -> int:
        """Property to get the number of inversion and check the solvability.

        Returns:
            int: number of inversion in the board.
        """
        nb_inv = 0
        for i, vali in enumerate(self.values):
            for valj in self.values[i+1:]:
                if not vali*valj:
                    continue
                nb_inv += int(valj < vali)
        return nb_inv

    def can_reach(self, other: 'Board') -> bool:
        """Compares the number of inversions to determine if a path exists between the two boards.

        Args:
            other (Board): Board to reach.

        Returns:
            bool: True if a path exists between the two boards.
        """
        return (self.nb_inv - other.nb_inv)%2 == 0

    def hamming(self, other: 'Board') -> int:
        """Compute the hamming distance.

        Args:
            other (Board): Board to compute the distance with.

        Returns:
            int: hamming distance between the two boards.
        """
        return sum(i != j for i, j in zip(self.values, other.values))

    @staticmethod
    def to_xy(index: int, size: int) -> Tuple[int, int]:
        """Static method to translate a position in the flattened list to two coordinates.

        Args:
            index (int): position in the flattened list.
            size (int): size of the board.

        Returns:
            int, int: coordinates of the index in two coordinates.
        """
        return index // size, index % size

    def manhattan(self, other: 'Board') -> int:
        """Compute the manhattan distance.

        Args:
            other (Board): Board to compute the distance with.

        Returns:
            int: manhattan distance between the two boards.
        """
        dist = 0
        for i, val in enumerate(self.values):
            cur_i, cur_j = Board.to_xy(i, self.size)
            other_i, other_j = Board.to_xy(other.values.index(val), self.size)
            dist += abs(cur_i-other_i) + abs(cur_j-other_j)
        return dist

    def neighbors(self) -> Generator['Board', None, None]:
        """A generator to yield the neighboring boards.

        Yields:
            Board: neighboring boards.
        """
        zero = self.values.index(0)
        i, j = Board.to_xy(zero, self.size)

        displacements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for delta_i, delta_j in displacements:
            new_i = i + delta_i
            new_j = j + delta_j
            if 0 <= new_i < self.size and  0 <= new_j < self.size:
                # Move is valid
                new_vals = list(self.values)
                new_zero = self.size*new_i+new_j
                new_vals[new_zero] = 0
                new_vals[zero] = self.values[new_zero]
                yield Board(tuple(new_vals))

    def __eq__(self, other: 'Board') -> bool:
        """__eq__ overloading

        Args:
            other (Board): Board to compare to.

        Returns:
            bool: True if Boards are equal.
        """
        return self.values == other.values

def create_standard_target_board(size: int) -> Board:
    """Small utility function to generate a standard (ordered) board.

    Args:
        size (int): size of the board (will result in size**2 elements in the board.)

    Returns:
        Board: standard board.
    """
    return Board(tuple(i for i in range(1, size**2))+(0,))

class State:
    """
    State class
    """

    __slots__ = ('board', 'nb_moves', 'previous', 'priority')

    def __init__(self, board: Board, nb_moves: int, previous: "State", priority: int):
        """State constructor

        Args:
            board (Board): board.
            nb_moves (int): number of moves to get there.
            previous (State): previous state.
            priority (int): priority of the state.
        """
        self.board = board
        self.nb_moves = nb_moves
        self.previous = previous
        self.priority = priority

    def reconstruct_path(self):
        """This function reconstructs the path to a given state.

        Returns:
            list of Board: list of all the boards in the history.
        """
        boards = []
        cur_state = self
        while cur_state:
            boards.append(cur_state.board)
            cur_state = cur_state.previous
        boards.reverse()
        return boards

    def __lt__(self, other: "State") -> bool:
        """__lt__ overload.

        Args:
            other (State): State to compare to.

        Returns:
            bool: comparison of the two state priorities.
        """
        return self.priority < other.priority
