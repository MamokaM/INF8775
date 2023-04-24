import numpy as np
import argparse

# enclosure class


class Enclosure:
    def __init__(self, id, size, is_in_subset, out_weights, in_weights, points):
        self.id = id
        self.size = size
        self.is_in_subset = is_in_subset
        self.out_weights = out_weights
        self.in_weights = in_weights
        self.points = points

    def calculateTotalWeight(self):
        return sum(self.out_weights) + sum(self.in_weights)

    def setStartingPoint(self, visited_points):
        if len(visited_points) == 0:
            self.points.append((0, 0))
            visited_points.append(0, 0)
        else:
            origin = (0, 0)
            placed = False
            reach = 1
            dest = (0, 0)
            while not placed:
                # Check top
                if (origin[0], origin[0] + reach) not in visited_points:
                    dest = (origin[0], origin[1] + reach)
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)
                # Check left
                elif (origin[0] - reach, origin[1]) not in visited_points:
                    dest = (origin[0] - reach, origin[1])
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)
                # Check right
                elif (origin[0] + reach, origin[1]) not in visited_points:
                    dest = (origin[0] + reach, origin[1])
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)

                reach = reach + 1

    def calculateWeightFromEnclosure(self, enclosure):
        return self.out_weights[enclosure.id] + self.in_weights[enclosure.id]

    def findHeaviestNeighborPossible(self, enclosures, in_subset):
        selected_neighbor = 0
        max_weight = 0
        for enclosure in enclosures:
            if in_subset and enclosure.is_in_subset and len(enclosure.points) == 0:
                if self.calculateWeightFromEnclosure(enclosure) > max_weight:
                    max_weight = self.calculateWeightFromEnclosure(enclosure)
                    selected_neighbor = enclosure.id
            elif not in_subset and len(enclosure.points) == 0:
                if self.calculateWeightFromEnclosure(enclosure) > max_weight:
                    max_weight = self.calculateWeightFromEnclosure(enclosure)
                    selected_neighbor = enclosure.id
        return enclosures[selected_neighbor]

    def grow(self, visited_points):
        if len(self.points) < self.size:
            origin = self.points[-1]
            placed = False
            dest = (0, 0)
            while not placed:
                # Check left
                if (origin[0] - 1, origin[1]) not in visited_points:
                    dest = (origin[0] - 1, origin[1])
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)
                # Check bottom
                elif (origin[0], origin[1] - 1) not in visited_points:
                    dest = (origin[0], origin[1] - 1)
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)
                # Check top
                elif (origin[0], origin[1] + 1) not in visited_points:
                    dest = (origin[0], origin[1] + 1)
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)
                # Check right
                elif (origin[0] + 1, origin[1]) not in visited_points:
                    dest = (origin[0] + 1, origin[1])
                    placed = True
                    visited_points.append(dest)
                    self.points.append(dest)


# initialise enclosures
def initialiseEnclosures(subset, sizes, weights):
    enclosures = []
    for id in range(0, len(sizes)):
        is_in_subset = searchInSubset(id, subset)
        size = sizes[id]
        out_weights = weights[id]
        in_weights = []
        for row in weights:
            in_weights.append(row[id])
        enclosures.append(
            Enclosure(id, size, is_in_subset, out_weights, in_weights, [])
        )
    return enclosures


# return true if enclosure is in subset
def searchInSubset(id, subset):
    for enclosure in subset:
        if id == enclosure:
            return True
    return False


# return heaviest enclosure
def selectFirstEnclosure(enclosures):
    selected_enclosure = 0
    max_weight = 0
    for enclosure in enclosures:
        if enclosure.is_in_subset:
            if enclosure.calculateTotalWeight() > max_weight:
                max_weight = enclosure.calculateTotalWeight()
                selected_enclosure = enclosure.id
    return enclosures[selected_enclosure]


# read file
def readFile(file):
    enclosures_number = 0
    subset_size = 0
    max_distance = 0
    subset = []
    sizes = []
    weights = []
    with open(file, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if i == 0:
                enclosures_number, subset_size, max_distance = map(
                    int, lines[i].split()
                )
            elif i == 1:
                subset = list(map(int, lines[i].strip().split()))
            elif i > 1 and i < enclosures_number + 2:
                index = i - 2
                sizes.append(int(lines[i].strip()))
            else:
                weights = np.resize(weights, (enclosures_number, enclosures_number))
                index = i - enclosures_number - 2
                weights[index, :] = lines[i].strip().split()
    return enclosures_number, subset_size, max_distance, subset, sizes, weights


################ main script #######################

if __name__ == "__main__":

     # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--file", required=True, type=str, help="Define the path of the exemplaire ")

    parser.add_argument(
        "-p",
        "--option",
        required=False,
        action="store_true",
        help="Display new best solution",
    )

    args = parser.parse_args()
    file_name = args.file

    # read file
    enclosures_number, subset_size, max_distance, subset, sizes, weights = readFile(file_name)

    # initialise enclosures
    enclosures = initialiseEnclosures(subset, sizes, weights)

    # select first enclosure and set position
    visited_points = []
    firstEnclosure = selectFirstEnclosure(enclosures)
    firstEnclosure.points.append((0, 0))
    visited_points.append((0, 0))

    generated_enclosures = []
    generated_enclosures.append(firstEnclosure)

    # select enclosures from subset and set position
    for i in range(0, subset_size - 1):
        nextEnclosure = firstEnclosure.findHeaviestNeighborPossible(enclosures, True)
        nextEnclosure.setStartingPoint(visited_points)
        generated_enclosures.append(nextEnclosure)

    # select enclosures from outside subset and set position
    for i in range(0, enclosures_number - subset_size):
        nextEnclosure = firstEnclosure.findHeaviestNeighborPossible(enclosures, False)
        nextEnclosure.setStartingPoint(visited_points)
        generated_enclosures.append(nextEnclosure)

    # grow cells
    for i in range(0, max(sizes)):
        for enclosure in generated_enclosures:
            enclosure.grow(visited_points)

   
    # # write solution
    with open("sol_" + str(enclosures_number) + "_" + str(subset_size) + ".txt", "w") as f:
        for enclosure in enclosures:
            for point in enclosure.points:
                f.write(str(point[0]) + " " + str(point[1]) + " ")
            f.write("\n")
        

    # NOTE : this is not usefull for our algorithm but we still implemented it since that is what was asked 
    if args.option:
        
        while(True):
            for enclosure in enclosures:
                for point in enclosure.points:
                    print(point[0], point[1], end='')
                print()
            print()
    else:

        for enclosure in enclosures:
            for point in enclosure.points:
                print(point[0], point[1], end='')
            print()

        while True:
            continue

