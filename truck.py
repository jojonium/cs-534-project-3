import collections
import random
from pprint import pprint
import sys


class TruckProblem:
    def __init__(self, truck_capacity, num_houses, start_penalty, time_limit):
        self.probability = 15
        self.warehouse = collections.deque()
        self.tick_counter = 0
        self.num_houses = num_houses
        self.truck_capacity = truck_capacity
        self.q_table = initializeQTable(truck_capacity)
        self.truck = {"location": 0, "packages": [], "delivering": False}
        self.time_limit = time_limit
        self.start_penalty = start_penalty
        self.current_score = 0
        self.total_score = 0
        self.epsilon = 0.8
        self.alpha = 0.1
        self.gamma = 0.9
        self.start_state = (0, 0)
        self.last_action = ""

    def start(self):
        while self.tick_counter < self.time_limit:
            self.tick()
            self.epsilon -= 0.8 / (self.time_limit * 0.9)
        pprint(self.q_table)
        print("Final score: {}".format(self.total_score))

    def choose_move(self):
        if random.random() < self.epsilon:
            if random.random() < 0.5:
                action = "WAIT"
            else:
                action = "DELIVER"
            best_q = self.q_table[(len(self.truck["packages"]), self.probability)][action]
        else:

            best_q = self.q_table[(len(self.truck["packages"]), self.probability)]["DELIVER"]
            action = "DELIVER"
            if self.q_table[(len(self.truck["packages"]), self.probability)]["WAIT"] == best_q:
                if random.random() < 0.5:
                    action = "WAIT"
                else:
                    action = "DELIVER"
                best_q = self.q_table[(len(self.truck["packages"]), self.probability)][action]
            elif self.q_table[(len(self.truck["packages"]), self.probability)]["WAIT"] >= best_q:
                action = "WAIT"
                best_q = self.q_table[(len(self.truck["packages"]), self.probability)]["WAIT"]
        return action, best_q

    def tick(self):
        print("tick {}".format(self.tick_counter))
        self.tick_counter += 1
        # if truck is at warehouse, packages are in warehouse and space in truck, then packages are loaded

        if self.truck["location"] == 0:
            while len(self.truck["packages"]) < self.truck_capacity and len(self.warehouse) > 0:
                print("loading packages at warehouse")
                self.truck["packages"].append(self.warehouse.pop())

        roll = random.random()
        if roll < self.probability / 100:
            package = {"timeCreated": self.tick_counter, "address": random.randint(0, self.num_houses) + 1}
            print("created package for {}".format(package["address"]))
            if self.truck["location"] == 0 and len(self.truck["packages"]) < self.truck_capacity:
                self.truck["packages"].append(package)
            else:
                self.warehouse.append(package)
            if self.probability < 25:
                self.probability += 2
        else:
            if self.probability > 5:
                self.probability -= 2

        if self.truck["delivering"]:
            if len(self.truck["packages"]) == 0:
                print("going back to warehouse, now at location {}".format(self.truck["location"]))
                self.truck["location"] = max(0, self.truck["location"] -1)
                if self.truck["location"] == 0:
                    # done delivering
                    print("back at warehouse and not delivering")
                    self.truck["delivering"] = False
            else:
                self.truck["location"] += 1
                previousPackages = len(self.truck["packages"])
                self.truck["packages"] = list(filter((lambda x: x["address"] != self.truck["location"]), self.truck["packages"]))
                numDelivers = previousPackages - len(self.truck["packages"])
                self.current_score += numDelivers * 30 * self.num_houses
                print("delivered {} at location {}".format(numDelivers, self.truck["location"]))
        else:
            action, best_q = self.choose_move()
            if action == "DELIVER":
                print("decided to start deliver >:D")
                self.truck["delivering"] = True
                self.start_state = (len(self.truck["packages"]), self.probability)
                self.last_action = "DELIVER"
                self.current_score += self.start_penalty
            else:
                print("decided to wait")
                # decided to wait, update table
                self.start_state = (len(self.truck["packages"]), self.probability)
                self.last_action = "WAIT"
        for package in self.warehouse:
            self.current_score -= self.tick_counter - package["timeCreated"]
        for package in self.truck["packages"]:
            self.current_score -= self.tick_counter - package["timeCreated"]

        if self.truck["location"] == 0:
            self.updateTable()
            print("new score is {}".format(self.total_score))
        return

    def updateTable(self):
        print("UPDATING TABLE")
        newState = (len(self.truck["packages"]), self.probability)
        future_best_q = max(self.q_table[newState]["WAIT"], self.q_table[newState]["DELIVER"])
        self.q_table[self.start_state][self.last_action] += \
            self.alpha * (self.current_score + self.gamma * future_best_q - self.q_table[self.start_state][self.last_action])
        self.total_score += self.current_score
        self.current_score = 0


def initializeQTable(truckCapacity):
    q_table = {}
    for n in range(truckCapacity + 1):
        for p in range(5, 25, 2):
            q_table[(n, p)] = {}
            q_table[(n, p)]["WAIT"] = 0
            q_table[(n, p)]["DELIVER"] = 0

    return q_table


def printUsage():
    print("Usage:")
    print("\tpython truck.py TRUCK_CAPACITY ROAD_LENGTH START_PENALTY NUM_TICKS")


if __name__ == '__main__':
    if len(sys.argv) < 5:
        printUsage()
        exit()
    else:
        t = TruckProblem(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        t.start()


