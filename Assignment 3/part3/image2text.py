#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Barza Fayazi-Azad (bfayazi), Kaavya Tejaswi (kpolukon), Nathaniel Priddy (ngpriddy)
# (based on skeleton code by D. Crandall, Oct 2020)
#
import copy

from PIL import Image
import math
import sys
import operator

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)


# Read in the text training data
def read_text():
    txt = train_txt_fname
    cleaned_data = []
    file = open(txt, 'r');
    for line in file:
        data = [word + ' ' for word in line.split()][::2]

        cleaned_data.append(data)

    return cleaned_data


# Initial state probabilities
def initial():
    data = read_text()
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    initial_state_counts = {}

    for line in data:
        for word in line:
            if word[0] in TRAIN_LETTERS:
                if word[0] not in initial_state_counts:
                    initial_state_counts[word[0]] = 1
                else:
                    initial_state_counts[word[0]] += 1

    # Percent of all words that start with each letter
    initial_state_probs = {}
    initial_total = sum(initial_state_counts.values())
    for letter in initial_state_counts:
        initial_state_probs[letter] = initial_state_counts[letter] / float(initial_total)

    return initial_state_probs


# transition probabilities
def transition():
    data = read_text()
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    transition_letters = {}

    # Output the number of transitions for specific letter pairs
    for line in data:
        for word in line:
            for i in range(len(word) - 1):
                if (word[i] in TRAIN_LETTERS and word[i + 1] in TRAIN_LETTERS) and (
                        word[i] + "-->" + word[i + 1]) in transition_letters:
                    transition_letters[word[i] + "-->" + word[i + 1]] += 1
                else:
                    if (word[i] in TRAIN_LETTERS and word[i + 1] in TRAIN_LETTERS):
                        transition_letters[word[i] + "-->" + word[i + 1]] = 1


    # Output the total appearances of each letter via transitions
    transition_count = {}
    for i in range(len(TRAIN_LETTERS)):
        count = 0

        # Loop through transitions dict and count appearances for each letter
        for letter in transition_letters:
            if (TRAIN_LETTERS[i] == letter.split('-->')[0]):
                count = count + transition_letters[letter]
            else:
                continue

        # Save final count
        if count > 0:
            transition_count[TRAIN_LETTERS[i]] = count


    # Create count percentages as count / total count
    total_count = sum(transition_count.values())
    for letter in transition_count:
        transition_count[letter] = transition_count[letter] / total_count


    # Create transition probabilities dict to find % that letter B follows letter A
    # i.e. 10 total appearances of "T", 7 of which are followed by "h", so T-->h = 0.7
    transition_probs = {}
    for letter in transition_letters:
        transition_probs[letter] = (transition_letters[letter]) / (float(transition_count[letter.split("-->")[0]]))


    transitions_probs_total = {}
    trans_total = sum(transition_probs.values())
    for pair in transition_probs:
        transitions_probs_total[pair] = transition_probs[pair] / float(trans_total)

    return transitions_probs_total




# Calculate the total ratio of black chars / all chars
# The higher the ratio, the more value needs to be placed on the opposite color correct performance to improve accuracy
# i.e. if test file is corrupted with lots of blacks, increase the white correct weight and decrease black correct weight
# and vice versa if test file is corrupted with lots of whites

def check_black_test(test_letters):
    black_test = 0
    test_total = 0
    for letter in test_letters:
        for line in letter:
            for char in line:
                test_total += 1
                if char == '*':
                    black_test += 1

    return [black_test,test_total]


def check_black_train(train_letters):
    black_train = 0
    train_total = 0
    for letter in train_letters:
        for line in train_letters[letter]:
            for char in line:
                train_total += 1
                if char == '*':
                    black_train += 1

    return [black_train,train_total]


# Emission probabilities

def emission(test_letters, train_letters):

    emission_probs = {}
    test_vals = check_black_test(test_letters)
    train_vals = check_black_train(train_letters)


    # Loop through test letters and train letters and create dictionary of emission probabilities
    for test_let in range(len(test_letters)):
        emission_probs[test_let] = {}
        for train_let in train_letters:
            black_correct = 0
            white_correct = 0
            total = CHARACTER_WIDTH * CHARACTER_HEIGHT
            # Need to loop through two levels
            for i in range(len(test_letters[test_let])):
                for x in range(len(test_letters[test_let][i])):
                    if test_letters[test_let][i][x] == train_letters[train_let][i][x] and train_letters[train_let][i][x] == '*':
                        black_correct += 1
                    if test_letters[test_let][i][x] == train_letters[train_let][i][x] and train_letters[train_let][i][x] == ' ':
                        white_correct += 1

                    # After some testing, for more corrupted files with lots of blacks, lowering black coefficient
                    # improves performance while for more corrupted files with lots of white, increasing black coefficient
                    # improves performance

                    if (test_vals[0]/test_vals[1]) > (train_vals[0]/train_vals[1]):
                        emission_probs[test_let][train_let] = 0.6*(black_correct / total) + 0.4*(white_correct/total)
                    else:
                        emission_probs[test_let][train_let] = 0.9 * (black_correct / total) + 0.1 * (
                                    white_correct / total)


    return emission_probs


# Output results from simple bayes net
def simple_bayes(test_letters, train_letters):
    output = ''
    emission_probs = emission(test_letters, train_letters)
    for val in emission_probs:
        output += ''.join(max(emission_probs[val], key = emission_probs[val].get))

    return output


# Output results from HMM using Viterbi algo
def hmm_viterbi(test_letters, train_letters):

    # Initialize initial state, transition, and emission probs
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    initial_state_probs = initial()
    transition_probs = transition()
    emission_probs = emission(test_letters,train_letters)

    # Initialize final output and viterbi matrix
    output = ['X'] * len(test_letters)
    viterbi = []

    for train_val in range(len(TRAIN_LETTERS)):
        sub_vit = []
        for test_val in range(len(test_letters)):
            sub_vit.append([0,''])
        viterbi.append(sub_vit)


    # Since emission probabilities performed well in Simple Bayes, we will only take top 5 higher probabilities per state
    # to improve run times

    # Get initial state using initial state probs
    top5 = dict(sorted(emission_probs[0].items(), key=operator.itemgetter(1), reverse=True)[:5])
    for train_val in range(len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[train_val] in initial_state_probs and TRAIN_LETTERS[train_val] in top5 and top5[TRAIN_LETTERS[train_val]] != 0:
            viterbi[train_val][0] = [-math.log10(top5[TRAIN_LETTERS[train_val]]),TRAIN_LETTERS[train_val]]

    # Remainder of states again taking top 5 emissions for each
    for test_val in range(1,len(test_letters)):
        top5 = dict(sorted(emission_probs[test_val].items(), key=operator.itemgetter(1), reverse=True)[:5])

        # Loop through each of the top 5 emissions and add them to the viterbi matrix with transition probs added
        for val in top5:
            sub_vit = {}
            for train_val in range(len(TRAIN_LETTERS)):
                if (TRAIN_LETTERS[train_val]+"-->"+val) in transition_probs and viterbi[train_val][test_val-1][0] != 0:
                    # Adding additional weights to emission probabilities since they performed well previously
                        sub_vit[val] = -30* math.log10(top5[val]) - 0.01*math.log10(transition_probs[TRAIN_LETTERS[train_val]+"-->"+val]) - 0.01*math.log10(viterbi[train_val][test_val-1][0])

            # Create our final viterbi matrix from the sub-viterbi for each state
            x = 99999
            for key in sub_vit:
                if x > sub_vit[key]:
                    x = sub_vit[key]
                    final_letter = key
                viterbi[TRAIN_LETTERS.index(val)][test_val] = [sub_vit[final_letter],final_letter]


    # Running through the viterbi matrix
    for test_val in range(len(test_letters)):
        # default large num to minimize
        x = 99999
        for train_val in range(len(TRAIN_LETTERS)):
            # Minimizing the cost - if the new value has a lower cost than the previous value for each state, replace the output with the new state (letter)
            if train_val < len(TRAIN_LETTERS) and viterbi[train_val][test_val][0] < x and viterbi[train_val][test_val][0] != 0:
                x = viterbi[train_val][test_val][0]
                output[test_val] = TRAIN_LETTERS[train_val]


    return ''.join(output)



print("Simple: {}".format(simple_bayes(test_letters,train_letters)))
print("HMM: {}".format(hmm_viterbi(test_letters,train_letters)))


