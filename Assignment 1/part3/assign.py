#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Barza Fayazi-Azad (bfayazi)
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#
import sys
import re
import random

# Read the survey results text file as a dictionary
def read_survey(file):
    survey_results = {}
    with open(file,'r') as f:
        for row in f.readlines():
            results = row.split()
            user, requested_team, users_to_avoid = results[0], results[1], results[2]
            survey_results[user] = [requested_team, users_to_avoid]

    return survey_results


# Split hyphenated string into list
def split_hyphen(team):
    return re.split(r'[\s-]+',team)


# Find the preferred team size of a student
def preferred_team_size(student,survey_results):
    return len(re.split(r'[\s-]+',survey_results[student][0]))


# Find the preferred team members of a student
def preferred_team_members(student, survey_results):
    pref_members = re.split(r'[\s-]+',survey_results[student][0])
    return [member for member in pref_members if member != 'xxx' and member != 'zzz']


# Find the unwanted team members of a student
def unwanted_team_members(student, survey_results):
    return survey_results[student][1].split(',')



# Calculate total cost of the group assignments
def total_cost(assignments, survey_results):
    sum_cost = 0

    # Grading time costs
    grading_cost = 5 * len(assignments)

    # Team size complaint costs
    team_size_cost = 0
    for student in survey_results.keys():
        for team in assignments:
            if student in team:
                if len(split_hyphen(team)) != preferred_team_size(student,survey_results):
                    team_size_cost = team_size_cost + 2

    # Cheating cost
    cheating_cost = 0
    for student in survey_results.keys():
        for team in assignments:
            if student in team:
                for partner in preferred_team_members(student, survey_results):
                    if partner not in split_hyphen(team):
                        cheating_cost = cheating_cost + (0.05*60)

    # Unwanted team member cost
    unwanted_cost = 0
    for student in survey_results.keys():
        for team in assignments:
            if student in team:
                for enemy in unwanted_team_members(student, survey_results):
                    if enemy in split_hyphen(team):
                        unwanted_cost = unwanted_cost + 10

    sum_cost = grading_cost + team_size_cost + cheating_cost + unwanted_cost

    return sum_cost


# Create groups with max 3 students in them
def random_grouping(students, num):
    initial_assignments = []
    cleaned_assignments = []
    assigned_students = []
    max_group_members = num

    # Randomly shuffle through the students and break when all students are assigned to a group
    random.shuffle(students)
    for i in range(len(students) // max_group_members + 1):
        if len(assigned_students) == len(students):
            break
        group = students[i * max_group_members:i * max_group_members + max_group_members]
        initial_assignments.append(group)
        for student in group:
            assigned_students.append(student)

    # Use delimiter to properly create groups for testing
    delim = "-"

    for group in initial_assignments:
        team = delim.join(group)
        cleaned_assignments.append(team)

    return cleaned_assignments





def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    # Read in the survey results
    survey_results = read_survey(input_file)
    students = list(survey_results.keys())

    # Empty visited group assignments
    visited_assignments = []

    # Initialize the first groups and get the cost
    first_groups = random_grouping(students,3)
    updated_cost = total_cost(first_groups, survey_results)
    lowest_cost_so_far = updated_cost

    # Initial solution
    solution = {'assigned-groups': first_groups
                , 'total-cost': updated_cost}


    while True:
        # Get a new set of groups (3)
        next_3_groups = random_grouping(students,3)
        if next_3_groups not in visited_assignments:
            visited_assignments.append(next_3_groups)
            updated_3_cost = total_cost(next_3_groups, survey_results)
        # Get a new set of groups (2)
        next_2_groups = random_grouping(students,2)
        if next_2_groups not in visited_assignments:
            visited_assignments.append(next_2_groups)
            updated_2_cost = total_cost(next_2_groups, survey_results)
        # Take the grouping with lower cost and keep that as new solution to test
        if updated_3_cost <= updated_2_cost:
            solution['assigned-groups'], solution['total-cost'] = next_3_groups, updated_3_cost
        else:
            solution['assigned-groups'], solution['total-cost'] = next_2_groups, updated_2_cost
        # If the latest solution has a lower cost than our lowest cost solution so far, yield solution and update lowest cost
        if solution['total-cost'] < lowest_cost_so_far:
            yield solution
            lowest_cost_so_far = solution['total-cost']






if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])

