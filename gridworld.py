import csv
import sys
import numpy as np


# Given a grid world, move cost, and probability of moving correctly,
# run the Q Learning algorithm for the given gridworld
def runQLearning(gridworld, move_cost, move_probability):
    qTable = initializeQTable(gridworld)
    startState = (0, gridworld.shape[1] - 1)

    # compute which allowed state is the most desirable to move to (highest Q value)
    bestQ = 0
    action = ''
    if startState[0] - 1 >= 0 and qTable[startState]["LEFT"] > bestQ:
        bestQ = qTable[startState]["LEFT"]
        action = "LEFT"
    if startState[0] + 1 < gridworld.shape[0] and qTable[startState]["RIGHT"] >= bestQ:
        bestQ = qTable[startState]["RIGHT"]
        action = "RIGHT"
    if startState[1] - 1 >= 0 and qTable[startState]["UP"] > bestQ:
        bestQ = qTable[startState]["UP"]
        action = "UP"
    if startState[1] + 1 < gridworld.shape[1] and qTable[startState]["DOWN"] > bestQ:
        bestQ = qTable[startState]["DOWN"]
        action = "DOWN"

    # actually perform the move (assume no stochasticity for now)
    if action == "LEFT":
        newState = (startState[0] - 1, startState[1])
    elif action == "RIGHT":
        newState = (startState[0] + 1, startState[1])
    elif action == "UP":
        newState = (startState[0], startState[1] - 1)
    else:
        newState = (startState[0], startState[1] + 1)

    # then, update Q value based on the state we ended up in
    if action == "LEFT":
        qTable[startState]["LEFT"] += 0.1 * (move_cost + 0.9 * (bestQ - qTable[startState]["LEFT"]))
    elif action == "RIGHT":
        qTable[startState]["RIGHT"] += 0.1 * (move_cost + 0.9 * (bestQ - qTable[startState]["RIGHT"]))
    elif action == "UP":
        qTable[startState]["UP"] += 0.1 * (move_cost + 0.9 * (bestQ - qTable[startState]["UP"]))
    else:
        qTable[startState]["DOWN"] += 0.1 * (move_cost + 0.9 * (bestQ - qTable[startState]["DOWN"]))

    # update which state we are in
    startState = newState


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