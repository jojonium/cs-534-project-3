import csv
import sys
import numpy as np


# Given a grid world, move cost, and probability of moving correctly,
# run the Q Learning algorithm for the given gridworld
def runQLearning(gridworld, move_cost, move_probability):
    qTable = initializeQTable(gridworld)
    startState = (0, gridworld.shape[1] - 1)


def initializeQTable(gridworld):
    qTable = {}
    for i in range(gridworld.shape[0]):
        for j in range(gridworld.shape[1]):
            qTable[(i, j)] = {}
            qTable[(i, j)]["UP"] = 0
            qTable[(i, j)]["DOWN"] = 0
            qTable[(i, j)]["LEFT"] = 0
            qTable[(i, j)]["RIGHT"] = 0

    return qTable


def printWorld(gridworld):
    print(gridworld.T)


def readFromFile():
    gridworld = []

    # read from csv
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            gridworld.append(np.array(np.float_(row)))

    return np.array(gridworld).T


def main():
    if len(sys.argv) < 4:
        # printUsage()
        exit()
    else:
        gridworld = readFromFile()
        move_cost = np.float_(sys.argv[2])
        move_probability = np.float_(sys.argv[3])

        runQLearning(gridworld, move_cost, move_probability)


if __name__ == '__main__':
    main()