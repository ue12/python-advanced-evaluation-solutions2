"""
This module implements the Solver class.
"""

import heapq

from puzzle8.board import Board, State, create_standard_target_board

class Solver:
    """
    Solver class.
    """
    def __init__(self, start_board: Board, target_board: Board = None, priority=Board.manhattan):
        """Solver constructor

        Args:
            start_board (Board): Start board.
            target_board (Board, optional): Target board, if None the standard one is used.
                Defaults to None.
            priority (callable, optional): Board method to compute the priority.
                Defaults to Board.manhattan.
        """
        self.start = start_board
        if target_board is None:
            target_board = create_standard_target_board(self.start.size)
        self.target = target_board
        self.priority = priority

    def check_consistency(self):
        """This method checks the consistency of the given data.

        Raises:
            ValueError: if start and target boards do not have the same size or if
                the priority callable does not give 0 when evaluated with twice the same board.
        """
        if self.start.size != self.target.size:
            raise ValueError("Sizes of start and target board are not consistent.")
        if self.priority(self.target, self.target) != 0:
            raise ValueError("The given priority should give 0 with twice the same board.")

    def solve(self):
        """
        This method solves the puzzle. It returns a dictionnary containing the solver results.
        Available keys in the dictionnary are :
         - reachable (bool): True if a path less than 36 moves long was found from start to target.
         - nb_moves (int): number of moves needed to reach target. Set to 200 000 if more than
           36 moves are needed.
         - moves (list of Board): all boards from start to target.

        Returns:
            dict: dictionnary containing the solver results.
        """
        self.check_consistency()

        if not self.start.can_reach(self.target):
            return dict(reachable=False, nb_moves=0, moves=[self.start])

        queue = []
        cur_state = State(board=self.start,
                          nb_moves=0,
                          previous=None,
                          priority=self.priority(self.start, self.target))

        heapq.heappush(queue, cur_state)

        # seen is a dictionnary containing the visited boards associated
        # to the number of moves to get there.
        seen = {self.start.values: 0}

        while queue:
            cur_state = heapq.heappop(queue)

            if cur_state.nb_moves >= 36:
                # We focus in the project on boards solvable in less than 36 moves
                continue

            if cur_state.board == self.target:
                # Target is reached !
                return dict(reachable=True,
                            nb_moves=cur_state.nb_moves,
                            moves=cur_state.reconstruct_path())

            for neigh in cur_state.board.neighbors():
                if seen.get(neigh.values, cur_state.nb_moves+2) < cur_state.nb_moves:
                    # We already have a shorter way to get to this board !
                    continue
                # Creating the stating and adding it to the priority queue.
                seen[neigh.values] = cur_state.nb_moves+1
                next_state = State(board=neigh,
                                   nb_moves=cur_state.nb_moves+1,
                                   previous=cur_state,
                                   priority=self.priority(neigh, self.target) + cur_state.nb_moves)
                heapq.heappush(queue, next_state)

        return dict(reachable=False, nb_moves=200_000, moves=[self.start])
