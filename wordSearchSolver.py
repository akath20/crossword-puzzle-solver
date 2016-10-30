"""
Author: Alex Atwater, 2015
"""

import pdb
import logging
import os
import sys



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
    if sys.version_info[0] < 3:
        user_input = raw_input("> ")
    else:
        user_input = input("> ")
    return user_input


def analyze(user_input):

    def add_coordinates(original_coord, displacement):
        return tuple(map(sum, zip(original_coord, displacement)))

    def valid_coord(coord_to_check):
        if all(((coord_to_check[0] >= 0), (coord_to_check[0] < (GRID_DIMENSION[0] + 1)),
                (coord_to_check[1] >= 0), (coord_to_check[1] < (GRID_DIMENSION[0] + 1)))):
            return True, coord_to_check
        else:
            return False, None

    def first_letter():  # find all coordinates that contain first letter
        first_letter_coord = []
        first_letter = user_input[0]
        for item in word_grid.items():  # if matching letter, add coordinates to list
            if item[1] == first_letter:
                first_letter_coord.append(item[0])
        logging.debug("first_letter(): {}".format(first_letter_coord))
        return first_letter_coord

    def second_letter(first_letter_coord):
        combinations_dict = {}
        for coordinate_to_check in first_letter_coord:
            # search all possible second letter combinations
            coordinates_to_check = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (1, -1), (0, -1), (-1, -1)]
            for mod_coordinate in coordinates_to_check:
                valid_coordinate_output = valid_coord(add_coordinates(coordinate_to_check, mod_coordinate))
                # if a valid coordinate
                if valid_coordinate_output[0]:
                    # check if there is a match. If there is one next to first letter, append and break loop
                    if word_grid[valid_coordinate_output[1]] == user_input[1]:
                        combinations_dict.setdefault(coordinate_to_check, []).append(
                            {"coordinate": valid_coordinate_output[1], "mod_coordinate": mod_coordinate})
        logging.debug(
            "NumPossibilities: {}\nsecond_letter(): {}".format(len(combinations_dict.keys()), combinations_dict)) # combinations_dict.keys() does not work here
        return combinations_dict

    def find_answer(combinations_dict):

        times_iter = (len(user_input) - 2)  # -2 because already did first and can't find next letter of last letter
        for potential_start_coordinate in combinations_dict.items():
            # iterate over the list of possibilities that deviate from start point
            for potential_next_coord_dict in enumerate(potential_start_coordinate[1]):
                curr_iter_count = 0
                start_iter_coord = potential_next_coord_dict[1]["coordinate"]
                mod_coordinate = potential_next_coord_dict[1]["mod_coordinate"]
                while curr_iter_count < times_iter:
                    # move up in the direction give
                    start_iter_coord = add_coordinates(start_iter_coord, mod_coordinate)
                    if not valid_coord(start_iter_coord)[0]:
                        break
                    # now check if the letter is the right letter
                    if word_grid[start_iter_coord] == user_input[curr_iter_count + 2]:
                        # if True, continue. Else, break and return to user
                        return potential_start_coordinate[0]
                    curr_iter_count += 1
        return "Nothing was found."
    return find_answer(second_letter(first_letter()))

while True:
    print(analyze(get_input()))
