"""
Author: Alex Atwater, 2015
"""

import pdb
import logging
import os

fileName = os.path.join(os.path.dirname(__file__), 'ws.txt')


logging.basicConfig(filename='dubug.log', level=logging.DEBUG)


# into
print("Welcome. Opening file {}", fileName)

# open file
wordFile = open(fileName, "r")
print("Opened file.")

# create grid dictionary and grid dimension
word_grid = {}
GRID_DIMENSION = (13, 13)

# minus 1 for starting at zero
GRID_DIMENSION = (GRID_DIMENSION[0] - 1, GRID_DIMENSION[1] - 1)

print("Analyzing file.")


for lineLoop in enumerate(wordFile):  # analyze each line
    lineList = list(lineLoop[1])
    # analyze every letter, put into grid
    for letterLoop in enumerate(lineList):
        # get attributes
        letterDimension = (lineLoop[0], letterLoop[0])
        letter = letterLoop[1]
        if letter == "\n":
            continue
        # add to dictionary
        word_grid[letterDimension] = letter
print("Grid complete, ready for input.")


def get_input():  # get input two letters
    user_input = input("> ")
    return user_input


def analyze(user_input):
    answerCoordinates = []

    def addCoordinates(originalCoordinate, displacement):
        return tuple(map(sum, zip(originalCoordinate, displacement)))

    def validCoordinate(coordinateToCheck):
        if all(((coordinateToCheck[0] >= 0), (coordinateToCheck[0] < (GRID_DIMENSION[0] + 1)),
                (coordinateToCheck[1] >= 0), (coordinateToCheck[1] < (GRID_DIMENSION[0] + 1)))):
            return (True, coordinateToCheck)
        else:
            return (False, None)

    def first_letter():  # find all coordinates that contain first letter
        first_letter_coord = []
        first_letter = user_input[0]
        for item in word_grid.items():  # if matching letter, add coordinates to list
            if item[1] == first_letter:
                first_letter_coord.append(item[0])
        logging.debug("firstLetter(): {}".format(first_letter_coord))
        return first_letter_coord

    def second_letter(first_letter_coord):
        combinationsDict = {}
        for coordinateToCheck in first_letter_coord:
            # search all possible second letter combinations
            coordinatesToCheck = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (1, -1), (0, -1), (-1, -1)]
            for modCoordinate in coordinatesToCheck:
                validCoordinateOutput = validCoordinate(addCoordinates(coordinateToCheck, modCoordinate))
                # if a valid coordinate
                if validCoordinateOutput[0]:
                    # check if there is a match. If there is one next to first letter, append and break loop
                    if word_grid[validCoordinateOutput[1]] == user_input[1]:
                        combinationsDict.setdefault(coordinateToCheck, []).append(
                            {"coordinate": validCoordinateOutput[1], "modCoordinate": modCoordinate})
                logging.debug(
                    "NumPossibilities: {}\nsecond_letter(): {}".format(len(combinationsDict.keys()), combinationsDict)) # combinationsDict.keys() does not work here
                return combinationsDict

        def find_answer(combinationsDict):

            times_iter = (len(user_input) - 2)  # -2 becuase already did first and can't find next letter of last letter
            for potentialStartCoordinate in combinationsDict.items():
                # iterate over the list of posibilities that deviate from start point
                for potentialNextCoordinateDict in enumerate(potentialStartCoordinate[1]):
                    currentIterateCount = 0
                    startIteratationCoordination = potentialNextCoordinateDict[1]["coordinate"]
                    modCoordinate = potentialNextCoordinateDict[1]["modCoordinate"]
                    while currentIterateCount < times_iter:
                        # move up in the direction give
                        startIteratationCoordination = addCoordinates(startIteratationCoordination, modCoordinate)
                        if validCoordinate(startIteratationCoordination)[0] == False:
                            break
                        # now check if the letter is the right letter
                        if word_grid[startIteratationCoordination] == user_input[currentIterateCount + 2]:
                            # if it's the right number, keep going. But if it came to an end, then stop everything and return to user.
                            return potentialStartCoordinate[0]
                        currentIterateCount += 1
            return "Nothing was found."
        return find_answer(second_letter(first_letter()))

while True:
    print(analyze(get_input()))