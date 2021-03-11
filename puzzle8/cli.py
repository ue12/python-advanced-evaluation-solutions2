"""
This module proposes a Command Line Interface.
"""

from argparse import ArgumentParser
import json
from math import sqrt

from puzzle8.board import Board
from puzzle8.solver import Solver

def create_board(filename):
    """This function reads a file and returns the board.

    Args:
        filename (str): filename.

    Returns:
        Board: Board contained in the file.
    """
    with open(filename, 'r') as fin:
        content = fin.read().replace('-', '0').replace('.', '0')
    values = tuple(int(s) for s in content.split())

    # Checking that the puzzle is a square
    root = int(sqrt(len(values)))
    if int(root+0.5)**2 != len(values):
        raise ValueError(f"The board in {filename} is not a square.")
    return Board(values=values)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="File in which the start board is stored.")
    parser.add_argument("output_file", type=str, help="Name of the output file")
    parser.add_argument("-t", "--target_file",
                        type=str,
                        help="File with the target if it is different from the standard one.",
                        default="")
    parser.add_argument("-d", "--distance",
                        type=str,
                        choices=["hamming", "manhattan"],
                        default="manhattan",
                        help="Priority to use. Default is manhattan")

    args = parser.parse_args()

    start = create_board(args.input_file)

    target = create_board(args.target_file) if args.target_file else None

    s = Solver(start_board=start, target_board=target, priority=Board.__dict__[args.distance])
    res = s.solve()


    with open(args.output_file, 'w') as f:
        print('\n\n'.join(str(bi) for bi in res["moves"]), file=f)
        print("---", file=f)
        del res["moves"]
        print(json.dumps(res), file=f)
