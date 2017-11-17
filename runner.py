#!/usr/bin/env python

"""
Common run script to apply algorithm to solve 2048 puzzle.
Algorithms are read from subdirectory algorithms and have to supply a function get_next_move(matrix), which should return a list of next moves.
"""

import os, sys
import logging
import argparse
import importlib
import pprint
import time
import tabulate
import random

import puzzle
import game_logic

from collections import defaultdict

def initializeGame(seed = None, showGUI = True):
    return puzzle.GameGrid(is_ai_game=True, seed = seed, showGUI = showGUI)

def printSummary(resultsDict):
    results = list(resultsDict.items())
    results.sort(key = lambda x: x[1]["Nmoves"], reverse=True)
    header = ["Algorithm name", "Score", "moves"]
    lines = [ [result[0], result[1]["score"], result[1]["Nmoves"]] for result in results ]
    print(tabulate.tabulate(lines, header, tablefmt="grid"))

def main(argv):
    parser = argparse.ArgumentParser( description = 'Script that applies a provided algorithm to solve 2048 puzzle.' ,
                                      formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( "-d", '--debug',       default = False, action='store_true', help = 'print in debug output' )
    parser.add_argument(       "--gui",         default = False, action="store_true", help = "shows graphical interface with current status")
    parser.add_argument(       "--ascii",       default = False, action="store_true", help = "prints current status to terminal")
    parser.add_argument(       "--sleep",       default = 0,                          help = "time to wait between moves [s].")
    parser.add_argument( "-s", "--seed",        default = None,                       help = "Set seed ot fixed value.")
    parser.add_argument( "-a", "--algorithm",   default = "example",                  help = "which algorithms to run. multiple algorithms can be split by ','.")
    parser.add_argument( "-r", "--runs",        default = 1,                          help = "How many games we run per algorithm. Scores are accumulated.")
    args = parser.parse_args(argv)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Set log level to DEBUG")
    else:
        logging.basicConfig(level=logging.INFO)

    results = defaultdict(lambda: {'score': 0, 'Nmoves': 0})  # algorithm name -> {'score': 4, 'Nmoves', 2}

    seed = args.seed
    if not seed:
        seed = [ random.choice(game_logic.all_directions) for i in range(17) ]

    args.runs = int(args.runs)

    for runIndex in range(args.runs):
        for algorithm in args.algorithm.split(","):

            logging.debug("Initializing game")
            gamegrid = initializeGame(seed = seed, showGUI = args.gui)

            logging.debug("loading algorithm " + algorithm)
            alg = importlib.import_module("algorithms."+algorithm)

            logging.debug("starting loop")
            done = False
            Nmoves = 0
            NnoMoves = 0
            while not done:
                logging.debug("Getting next move from algorithm")
                move = alg.get_next_move(gamegrid.game_model.mat)
                changed = gamegrid.ai_move(move)
                if not changed:
                    done = True
                    continue

                Nmoves += 1
                NnoMoves = 0

                time.sleep(float(args.sleep))

                # update game grid
                if args.gui:
                    gamegrid.update()
                if args.ascii:
                    print("status: (Score = {})".format(gamegrid.calc_score()))
                    print(tabulate.tabulate(gamegrid.game_model.mat, tablefmt="grid"))

                if gamegrid.game_over():
                    done = True
                    break

            score = gamegrid.calc_score()
            results[algorithm]['score'] += score
            results[algorithm]['Nmoves'] += Nmoves
            print("GAME OVER. Final score: {:8.0f} after {:5.0f} moves (algorithm: {}).".format(score, Nmoves, algorithm))

        printSummary(results)

    if args.gui:
        input("Press Enter to terminate.")

if __name__ == "__main__":
    main( sys.argv[1:] )
