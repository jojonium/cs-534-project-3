import collections
import random


#truck needs to know where it's at, and the packages it has


def tick(truck, truckCapacity, probability, warehouse: collections.deque, tickcounter, numHouses):
    print("in tick method")
    tickcounter += 1
    #if truck is at warehouse, packages are in warehouse and space in truck, then packages are loaded

    if truck["location"] == 0:
        while len(truck["packages"]) < truckCapacity and len(warehouse) > 0:
            print("loading packages at warehouse")
            truck["packages"].append(warehouse.pop())

    roll = random.random()
    if roll < probability:
        package = {"timeCreated": tickcounter, "address": random.randint(0, numHouses) + 1}
        print("created package for {}".format(package["address"]))
        if truck["location"] == 0 and len(truck["packages"]) < truckCapacity:
            truck["packages"].append(package)
        else:
            warehouse.append(package)
        if probability < 0.25:
            print("probability changed mwaha :P")
            probability += 0.02
    else:
        if probability > 0.05:
            probability -= 0.02

    if truck["delivering"]:
        if len(truck["packages"]) == 0:
            if truck["location"] > 0:
                print("going back to warehouse")
                truck["location"] -= 1
            else:
                print("back at warehouse and not delivering")
                truck["delivering"] = False
        else:
            truck["location"] += 1
            previousPackages = len(truck["packages"])
            truck["packages"] = list(filter((lambda x: x["address"] != truck["location"]), truck["packages"]))
            numDelivers = previousPackages - len(truck["packages"])
            print("delivered {} at location {}".format(numDelivers, truck["location"]))
    else:
        # TODO decide what to do next
        roll = random.random()
        if roll < 0.1:
            print("decided to start deliver >:D")
            truck["delivering"] = True
    return truck, probability, warehouse, tickcounter


def main():
    probability = 0.15
    warehouse = collections.deque()
    tickcounter = 0
    numHouses = 10
    truckCapacity = 10
    truck = {"location": 0, "packages": [], "delivering": False}
    timeLimit = 500

    while tickcounter < timeLimit:
        truck, probability, warehouse, tickcounter = tick(truck, truckCapacity, probability, warehouse, tickcounter, numHouses)


if __name__ == '__main__':
    main()