# SeekTruth.py : Classify text objects into two categories
#
# Polukonda Kavya Tejaswi (kpolukon), Nathaniel Priddy (ngpriddy),Barza Fayazi-Azad (bfayazi)
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import time


def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated class label for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#

def classifier(train_data, test_data):
    
    # This is just dummy code -- put yours here!
    frequency = {}
    train_length = len(train_data["objects"])
    for index in range(train_length):
        string = train_data["objects"][index]
        parsed_string = string.strip().lower().split()
        for term in parsed_string:
            if term not in frequency:
                frequency[term] = dict()

                
            if train_data["labels"][index] == "deceptive":
                if 'deceptive' not in frequency[term]:
                    frequency[term]['deceptive'] = 0
                frequency[term]["deceptive"] += 1
            else:
                if 'truthful' not in frequency[term]:
                    frequency[term]['truthful'] = 0
                
                frequency[term]["truthful"] += 1
                
                
    final = []
    test_length = len(test_data['objects'])
    for index in range(test_length):
        string = test_data['objects'][index]
        ratio = 1
        parsed_string = string.strip().lower().split()
        for term in parsed_string:
            if term not in frequency:
                continue
            else:
                if 'deceptive' not in frequency[term] or 'truthful' not in frequency[term]:
                    continue
                else:
                    div = frequency[term]['truthful'] / frequency[term]['deceptive']
                    ratio *= div
        if (ratio > 1):
            final.append('truthful')
        else:
            final.append('deceptive')

    return final

    


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([(results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"]))])
    #print(correct_ct)
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))

    

