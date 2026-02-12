# This file will where the user can play with the trained agents
# Running the file with paramer level_index will start the game at that level
# e.g. python play_with_agents.py 3, default is level 0

from game.main import Game
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--level_index', type=int, default=0, help='Index of the level to start the game from')
args = parser.parse_args()

if __name__ == "__main__":
    Game(args.level_index).run()
    