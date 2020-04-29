import collections
import random
import sys


class TruckProblem:
    def __init__(self, truck_capacity, num_houses, start_penalty, time_limit):
        self.probability = 15
        self.warehouse = collections.deque()
        self.tick_counter = 0
        self.num_houses = num_houses
        self.truck_capacity = truck_capacity
        self.q_table = QTable()
        self.truck = {"location": 0, "packages": [], "delivering": False}
        self.time_limit = time_limit
        self.start_penalty = start_penalty
        self.current_score = 0
        self.total_score = 0
        self.epsilon = 0
        self.alpha = 0.3
        self.gamma = 0.6
        self.start_state = (0, 0)
        self.last_action = ""

    def start(self):
        while self.tick_counter < self.time_limit:
            self.tick()
        self.total_score += self.current_score
        self.q_table.print()
        print("Final score: {}".format(self.total_score))

    def choose_move(self):
        q_deliver = self.q_table.getEntry(packageDistribution(self.truck["packages"], self.num_houses))["DELIVER"]
        q_wait = self.q_table.getEntry(packageDistribution(self.truck["packages"], self.num_houses))["WAIT"]
        if len(self.truck["packages"]) == self.truck_capacity:
            # always deliver if truck is full
            action = "DELIVER"
            best_q = q_deliver
        elif random.random() < self.epsilon:
            # chance for random explore
            if random.random() < 0.5:
                action = "WAIT"
                best_q = q_wait
            else:
                action = "DELIVER"
                best_q = q_deliver
        else:
            if q_deliver > q_wait:
                action = "DELIVER"
                best_q = q_deliver
            elif q_deliver == q_wait:
                # tied, choose randomly
                if len(self.truck["packages"]) > 0 and random.random() < 0.25:
                    action = "DELIVER"
                    best_q = q_deliver
                else:
                    action = "WAIT"
                    best_q = q_wait
            else:
                action = "WAIT"
                best_q = q_wait
        return action, best_q

    def tick(self):
        should_update = False
        self.tick_counter += 1
        # if truck is at warehouse, packages are in warehouse and space in truck, then packages are loaded

        if self.truck["location"] == 0:
            while len(self.truck["packages"]) < self.truck_capacity and len(self.warehouse) > 0:
                self.truck["packages"].append(self.warehouse.pop())

        roll = random.random()
        if roll < self.probability / 100:
            package = {"timeCreated": self.tick_counter, "address": random.randint(1, self.num_houses)}
            if self.truck["location"] == 0 and len(self.truck["packages"]) < self.truck_capacity:
                self.truck["packages"].append(package)
            else:
                self.warehouse.append(package)
            self.probability = min(25, self.probability + 2)
        else:
            self.probability = max(5, self.probability - 2)

        if self.truck["delivering"]:
            if len(self.truck["packages"]) == 0:
                self.truck["location"] = max(0, self.truck["location"] -1)
                if self.truck["location"] == 0:
                    # done delivering
                    should_update = True
                    self.truck["delivering"] = False
            else:
                self.truck["location"] += 1
                previousPackages = len(self.truck["packages"])
                self.truck["packages"] = list(filter((lambda x: x["address"] != self.truck["location"]), self.truck["packages"]))
                numDelivers = previousPackages - len(self.truck["packages"])
                self.current_score += numDelivers * 30 * self.num_houses
        else:
            action, best_q = self.choose_move()
            if action == "DELIVER":
                self.truck["delivering"] = True
                self.last_action = "DELIVER"
                self.current_score += self.start_penalty
            else:
                should_update = True
                self.last_action = "WAIT"
            self.start_state = packageDistribution(self.truck["packages"], self.num_houses)
        for package in self.warehouse:
            self.current_score -= self.tick_counter - package["timeCreated"]
        for package in self.truck["packages"]:
            self.current_score -= self.tick_counter - package["timeCreated"]

        if should_update:
            self.updateTable()
        return

    def updateTable(self):
        new_state = packageDistribution(self.truck["packages"], self.num_houses)
        future_best_q = max(self.q_table.getEntry(new_state)["WAIT"], self.q_table.getEntry(new_state)["DELIVER"])
        old_value = self.q_table.getEntry(self.start_state)[self.last_action]
        new_value = old_value + self.alpha * (self.current_score + self.gamma * future_best_q - old_value)
        self.q_table.updateEntry(self.start_state, self.last_action, new_value)
        self.total_score += self.current_score
        self.current_score = 0


class QTable:
    def __init__(self):
        self.q_table = {}

    def getEntry(self, package_tuple):
        if package_tuple not in self.q_table:
            self.q_table[package_tuple] = {}
            self.q_table[package_tuple]["WAIT"] = 0
            self.q_table[package_tuple]["DELIVER"] = 0
        return self.q_table[package_tuple]

    def updateEntry(self, package_tuple, action, updated_value):
        self.q_table[package_tuple][action] = updated_value

    def getQTable(self):
        return self.q_table

    def print(self):
        prefer_deliver = []
        prefer_wait = []
        for key, value in self.q_table.items():
            if value["DELIVER"] > value["WAIT"]:
                prefer_deliver.append(key)
            else:
                prefer_wait.append(key)
        print("States where we prefer to wait: {}".format(prefer_wait))
        print("States where we prefer to deliver: {}".format(prefer_deliver))


def packageDistribution(packages, road_length):
    # make the tuple
    num_groups = 1
    package_dist = [0 for n in range(num_groups)]
    for p in packages:
        for n in range(num_groups):
            if p["address"] <= road_length / num_groups * (n+1):
                package_dist[n] += 1
                break
    return tuple(package_dist)


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


