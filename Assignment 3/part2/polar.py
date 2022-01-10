#!/usr/local/bin/python3
#
# Authors: Nathaniel Priddy / ngpriddy
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = image.copy()
    new_image = draw_boundary(new_image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

def emission_probability(image_array, edge_weights, row, column):
    strength = edge_weights[row][column]
    strength_max = max(edge_weights[:,column])
    strength_prob = strength / strength_max

    point = image_array[row][column]
    point_max = max(image_array[:,column])
    point_prob = (1 - (point / point_max))**2

    emission_prob = strength_prob * (point_prob)
    return emission_prob

def transition_prob(air_chosen, ice_chosen, row):
    prev_air = 0
    prev_ice = 0

    # Setting to one prevents this from affecting the first point
    air_pos_prob = 1
    ice_pos_prob = 1

    # Calculate transition probability            
    if len(air_chosen) and len(ice_chosen):
        # Pull the last chosen points
        prev_air = air_chosen[-1]
        prev_ice = ice_chosen[-1]                

        #
        if prev_air != row:
            air_pos_prob = 1 / (abs(row - prev_air))
        if prev_ice != row:
            ice_pos_prob = 1 / (abs(row - prev_ice))

        air_pos_prob = sqrt(air_pos_prob**2)
        ice_pos_prob = sqrt(ice_pos_prob**2)

    return air_pos_prob, ice_pos_prob

def combine_prob(rows, air_chosen, ice_chosen, column, image_array, edge_weights):
    fringe = []
    for row in range(0, rows):
        # Calculate transition probability
        air_pos_prob, ice_pos_prob = transition_prob(air_chosen, ice_chosen, row)

        # Calculate emission probablity for choosing this point as a border
        emission_prob = emission_probability(image_array, edge_weights, row, column)

        # Calculate respective air, ice prob for the point. We calculate and save them seperately, so our max doesn't get confused with the lower points
        air_vert_prob = emission_prob * air_pos_prob
        ice_vert_prob = emission_prob * ice_pos_prob
        fringe.append((row, air_vert_prob, ice_vert_prob))

    air_chosen_one = max(fringe, key=lambda x:x[1])
    next_ice = 0
    if (air_chosen_one[0] + 10 ) >= 175:
        next_ice = air_chosen_one[0] + 1
    else:
        next_ice = air_chosen_one[0] + 11
    ice_chosen_one = max(fringe[next_ice:], key=lambda x:x[2])

    return air_chosen_one, ice_chosen_one

def simple_bayes_net(image_array, edge_weights):
    air_chosen = []
    ice_chosen = []

    rows = image_array.shape[0]
    columns = image_array.shape[1]

    for column in range(0, columns):
        fringe = []
        for row in range(0, rows):
            # Calculate emission probablity for choosing this point as a border
            emission_prob = emission_probability(image_array, edge_weights, row, column)
            fringe.append((row, emission_prob))

        air_chosen_one = max(fringe, key=lambda x:x[1])
        
        next_ice = 0
        if (air_chosen_one[0] + 10 ) >= 175:
            next_ice = air_chosen_one[0] + 1
        else:
            next_ice = air_chosen_one[0] + 11
        ice_chosen_one = max(fringe[next_ice:], key=lambda x:x[1])

        air_chosen.append(air_chosen_one[0])
        ice_chosen.append(ice_chosen_one[0])

    return air_chosen, ice_chosen

def hmm(image_array, edge_weights):
    air_chosen = []
    ice_chosen = []

    rows = image_array.shape[0]
    columns = image_array.shape[1]

    for column in range(0, columns):
        air_chosen_one, ice_chosen_one = combine_prob(rows, air_chosen, ice_chosen, column, image_array, edge_weights)

        air_chosen.append(air_chosen_one[0])
        ice_chosen.append(ice_chosen_one[0])

    return air_chosen, ice_chosen

def hmm_feedback(image_array, edge_weights, airice_feedback, icerock_feedback):
    air_chosen = []
    ice_chosen = []

    rows = image_array.shape[0]
    columns = image_array.shape[1]

    air_chosen.append(airice_feedback[1]) 
    ice_chosen.append(icerock_feedback[1]) 

    for column in range(airice_feedback[0]-1, 0, -1):
        air_chosen_one, dont_need = combine_prob(rows, air_chosen, [0], column, image_array, edge_weights)
        air_chosen.append(air_chosen_one[0])

    for column in range(icerock_feedback[0]-1, 0, -1):
        dont_need, ice_chosen_one = combine_prob(rows, [0], ice_chosen, column, image_array, edge_weights)
        ice_chosen.append(ice_chosen_one[0])

    air_chosen = air_chosen[::-1]
    ice_chosen = ice_chosen[::-1]

    for column in range(airice_feedback[0]+1, columns):
        air_chosen_one, dont_need = combine_prob(rows, air_chosen, [0], column, image_array, edge_weights)
        air_chosen.append(air_chosen_one[0])

    for column in range(icerock_feedback[0]+1, columns):
        dont_need, ice_chosen_one = combine_prob(rows, [0], ice_chosen, column, image_array, edge_weights)
        ice_chosen.append(ice_chosen_one[0])

    return air_chosen, ice_chosen

# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # Assign each prediction using their respective algorithm
    airice_simple, icerock_simple = simple_bayes_net(image_array, edge_strength)
    airice_hmm, icerock_hmm = hmm(image_array, edge_strength)
    airice_feedback, icerock_feedback = hmm_feedback(image_array, edge_strength, gt_airice, gt_icerock)

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
