import csv
import sys
import random
import time

import numpy as np


def choose_move(x, y, epsilon, qTable, gridworld):
    # compute which allowed state is the most desirable to move to (highest Q value)
    bestQ = float("-inf")
    action = ''
    if random.random() < epsilon:
        legal_moves = []
        if x - 1 >= 0:
            legal_moves.append("LEFT")
        if x + 1 < gridworld.shape[0]:
            legal_moves.append("RIGHT")
        if y - 1 >= 0:
            legal_moves.append("UP")
        if y + 1 < gridworld.shape[1]:
            legal_moves.append("DOWN")
        action = random.choice(legal_moves)
        bestQ = qTable[(x, y)][action]
    else:
        legal_moves = []
        if x - 1 >= 0 and qTable[(x, y)]["LEFT"] > bestQ:
            legal_moves = ["LEFT"]
            bestQ = qTable[(x, y)]["LEFT"]
        elif x - 1 >= 0 and qTable[(x, y)]["LEFT"] == bestQ:
            legal_moves.append("LEFT")
        if x + 1 < gridworld.shape[0] and qTable[(x, y)]["RIGHT"] > bestQ:
            legal_moves = ["RIGHT"]
            bestQ = qTable[(x, y)]["RIGHT"]
        elif x + 1 < gridworld.shape[0] and qTable[(x, y)]["RIGHT"] == bestQ:
            legal_moves.append("RIGHT")
        if y - 1 >= 0 and qTable[(x, y)]["UP"] > bestQ:
            legal_moves = ["UP"]
            bestQ = qTable[(x, y)]["UP"]
        elif y - 1 >= 0 and qTable[(x, y)]["UP"] == bestQ:
            legal_moves.append("UP")
        if y + 1 < gridworld.shape[1] and qTable[(x, y)]["DOWN"] > bestQ:
            legal_moves = ["DOWN"]
            bestQ = qTable[(x, y)]["DOWN"]
        elif y + 1 < gridworld.shape[1] and qTable[(x, y)]["DOWN"] == bestQ:
            legal_moves.append("DOWN")
        action = random.choice(legal_moves)

    return action, bestQ


# Given a grid world, move cost, and probability of moving correctly,
# run the Q Learning algorithm for the given gridworld
def runQLearning(gridworld, move_cost, move_probability, qTable, epsilon):
    startState = (0, gridworld.shape[1] - 1)
    total_move_cost = 0
    alpha = 0.1
    gamma = 0.9
    policy = []

    while True:

        action, bestQ = choose_move(startState[0], startState[1], epsilon, qTable, gridworld)

        # actually perform the move (assume no stochasticity for now)
        if action == "LEFT":
            newState = (startState[0] - 1, startState[1])
        elif action == "RIGHT":
            newState = (startState[0] + 1, startState[1])
        elif action == "UP":
            newState = (startState[0], startState[1] - 1)
        else:
            newState = (startState[0], startState[1] + 1)
        total_move_cost += move_cost

        # then, update Q value based on the state we ended up in
        future_best_q = max(qTable[newState].values())
        qTable[startState][action] +=\
            alpha * (move_cost + gridworld[newState[0]][newState[1]] + gamma * future_best_q - bestQ)

        # update which state we are in
        policy.append(action)
        startState = newState

        if gridworld[startState[0], startState[1]] != 0:
            #  reached a terminal state
            return qTable, gridworld[startState[0]][startState[1]] + total_move_cost, policy


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


def printUsage():
    print("Usage:")
    print("\tpython gridworld FILE MOVE_COST MOVE_PROBABILITY")


def main():
    if len(sys.argv) < 4:
        printUsage()
        exit()
    else:
        gridworld = readFromFile()
        move_cost = np.float_(sys.argv[2])
        move_probability = np.float_(sys.argv[3])

        qTable = initializeQTable(gridworld)
        epsilon = 0.8
        iterations = 0
        convergence_counter = 0
        old_reward = float("nan")
        start_time = time.time()
        while True:
            iterations += 1
            epsilon -= 0.8 / 1000
            qTable, reward, policy = runQLearning(gridworld, move_cost, move_probability, qTable, epsilon)
            if reward == old_reward:
                convergence_counter += 1
                if convergence_counter >= 3:
                    print("Converged after {} iterations".format(iterations))
                    print("Expected reward: {}".format(reward))
                    print("Policy: {}".format(policy))
                    return
            else:
                old_reward = reward
                convergence_counter = 0
            if time.time() - start_time >= 20:
                print("Ran out of time after {} iterations".format(iterations))
                print("Expected reward: {}".format(reward))
                print("Policy: {}".format(policy))
                return


if __name__ == '__main__':
    main()
