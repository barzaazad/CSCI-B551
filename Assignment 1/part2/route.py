#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name Barza Fayazi-Azad (bfayazi)
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#

import sys
from math import sqrt
from math import tanh
import heapq
import numpy as np


# Read the road segments file as a dictionary
def read_road_segments(file):
    road_segments = {}
    with open(file, 'r') as f:
        for row in f.readlines():
            # use split method since a "row" is only separated by spaces
            road_seg = row.split()
            city1 = road_seg[0]
            city2 = road_seg[1]
            # Check if city 1 in dict
            city1_ind = road_segments.get(city1)
            if not city1_ind:
                road_segments[city1] = {}
            # Check if city 2 in dict
            city2_ind = road_segments.get(city2)
            if not city2_ind:
                road_segments[city2] = {}
            # Adding the additional info (distance, speed limit, highway name)
            # Both ways need to be added since we are to assume all routes are 2-way
            road_segments[city1][city2] = (float(road_seg[2]), float(road_seg[3]), road_seg[4])
            road_segments[city2][city1] = (float(road_seg[2]), float(road_seg[3]), road_seg[4])

    return road_segments


# Read the city gps file as a dictionary
def read_city_gps(file):
    city_gps = {}
    with open(file ,'r') as f:
        for row in f.readlines():
            location = row.split()
            city, lat, long = location[0], float(location[1]), float(location[2])
            city_gps[city] = {lat, long}

    return city_gps



# Since cities will be defined by latitude and longitude, I'll use euclidean distance as the heuristic
def euclidean_distance(city1_coords, city2_coords):
    lat1,long1 = city1_coords
    lat2,long2 = city2_coords

    return sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)


# Calculate the euclidean distance between two cities using latitude and longitude
def cities_distance(city1, city2, city_gps):
    # If the city is not in the gps file, return 0
    # Going under the assumption that cities not in the city_gps file are "highways"
    # and therefore should be preferred for use when necessary
    if city1 not in city_gps.keys() or city2 not in city_gps.keys():
        return 0
    cities = tuple(sorted((city1, city2)))
    city1_coords, city2_coords = city_gps.get(cities[0]), city_gps.get(cities[1])

    return euclidean_distance(city1_coords, city2_coords)

# Find max speed limit in road segments file
# Previously, I had used 80 as max speed limit since that is the US limit and it will always underestimate
# but that way might have been reducing the time too drastically,
# so I decided to switch to the max speed limit within the road segments file in order to keep times more realistic
# while continuing to ensure underestimation

# Using numpy's genfromtxt method to load data from txt file and convert data into values
# Then I can take the max value from the 4th column (aka speed limit column)
def find_max_speed(file):
    city1, city2, distance, speed_limit, highway = np.genfromtxt(file, unpack=True)
    return max(speed_limit)

# Segment cost function
def segment_cost_function(end, current_state, city_gps, road_segments, max_speed):
    current_route, route_taken, current_segment_count, current_miles, current_time, current_delivery_time = current_state
    return current_segment_count + 1


# Distance cost function
def dist_cost_function(end, current_state, city_gps, road_segments, max_speed):
    current_route, route_taken, current_segment_count, current_miles, current_time, current_delivery_time = current_state
    current_city = current_route[-1]
    distance = cities_distance(current_city, end, city_gps)
    return current_miles + distance


# Time cost function
def time_cost_function(end, current_state, city_gps, road_segments, max_speed):
    current_route, route_taken, current_segment_count, current_miles, current_time, current_delivery_time = current_state
    current_city = current_route[-1]
    distance = cities_distance(current_city, end, city_gps)

    time = distance / max_speed
    return current_time + time


def delivery_cost_function(end, current_state, city_gps, road_segments, max_speed):
    current_route, route_taken, current_segment_count, current_miles, current_time, current_delivery_time = current_state
    current_city = current_route[-1]
    distance = cities_distance(current_city, end, city_gps)

    time = distance / max_speed
    return current_delivery_time + time



# Select the proper cost function
def cost_function_selection(cost_func, end, current_state, city_gps, road_segments, max_speed):
    if cost_func == 'segments':
        return segment_cost_function(end, current_state, city_gps, road_segments, max_speed)
    if cost_func == 'distance':
        return dist_cost_function(end, current_state, city_gps, road_segments, max_speed)
    if cost_func == 'time':
        return time_cost_function(end, current_state, city_gps, road_segments, max_speed)
    else:
        return delivery_cost_function(end, current_state, city_gps, road_segments, max_speed)


# All of the successors of a city = all the cities that are able to be directly visited from a city
def successors(city, road_segments):
    return road_segments[city].keys()


# Check if our most recently visited city is the defined end city and therefore a goal state
def is_goal(current_route, end_city):
    return current_route[-1] == end_city




def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # Read in the two text files
    road_segments = read_road_segments('road-segments.txt')
    city_gps = read_city_gps('city-gps.txt')

    # Initialize an empty fringe
    fringe = []

    # Keep track of visited cities and what the cost function was when it was visited
    # This will allow us to "re-visit" cities if we come across a more optimal path that runs through it
    visited_cities = {}
    cost_function_of_visited = {}

    # Keep track of the route - will be initialized as the start city
    current_route = [start]

    # Keep track of the route taken (including cities, highways, distances)
    route_taken = []

    # Initialize all of our cost function variables
    current_segment_count = 0
    current_miles = 0
    current_time = 0
    current_delivery_time = 0

    # Find max speed limit for calculations
    max_speed = find_max_speed('road-segments.txt')


    # Insert starting elements into the fringe, using heapq module again
    starting_fringe_vals = (current_route, route_taken, current_segment_count, current_miles, current_time, current_delivery_time)
    updated_cost_function = cost_function_selection(cost, end, starting_fringe_vals, city_gps, road_segments, max_speed)
    heapq.heappush(fringe, (updated_cost_function, starting_fringe_vals))

    # while fringe is populated
    while fringe:
        # Pop out elements from fringe
        updated_cost_function, (current_route, route_taken, current_segment_count, current_miles, current_time, current_delivery_time) = heapq.heappop(fringe)
        # Check if you're at the end city (aka goal state) by taking the most recent (last) value from the current_route
        if is_goal(current_route, end):
            return {"total-segments": len(route_taken),
                    "total-miles": current_miles,
                    "total-hours": current_time,
                    "total-delivery-hours": current_delivery_time,
                    "route-taken": route_taken}

        # If we haven't reached a goal state and city is unvisited, add it to the visited dict
        if current_route[-1] not in visited_cities.keys():
            visited_cities[current_route[-1]] = True

        # Record what the value of the cost function is at the current visited city
        cost_function_of_visited[current_route[-1]] = updated_cost_function
        # Successors of the current city
        successor_cities = successors(current_route[-1], road_segments)
        for city in successor_cities:
            miles, speed_limit, highway = road_segments[current_route[-1]][city]
            time = miles / speed_limit
            # If speed limit of highway is >= 50, then calculate adjusted delivery time
            if speed_limit >= 50:
                delivery_time = time + tanh(miles/1000)*2*(time + current_delivery_time)
            # Otherwise, delivery time is same as normal time
            else:
                delivery_time = time

            # Next value in the fringe
            next_value_fringe = (current_route + [city], route_taken + [(str(city),str(highway) + " for " + str(miles) + " miles")]
                                 ,current_segment_count + 1, current_miles + miles,
                                   current_time + time, current_delivery_time + delivery_time)

            # Updated cost function value based on next fringe value
            updated_cost_function = cost_function_selection(cost, end, next_value_fringe, city_gps, road_segments, max_speed)

            # If we are trying to minimize miles, time, or delivery time, it is possible to revisit a city if the new path
            # has a lower cost function than when we originally visited the city
            # This if statement will allow us to revisit cities if the situation listed above occurs
            if city not in visited_cities.keys():
                heapq.heappush(fringe, (updated_cost_function, next_value_fringe))
            else:
                # Segments is always increasing by 1 regardless, so no need to revisit if that's the cost function
                # If new cost function of city is less than cost function when we previously visited
                if cost != 'segments' and updated_cost_function < cost_function_of_visited[city]:
                    # Change visited val to False (aka allow us to revisit)
                    visited_cities[city] = False
                    heapq.heappush(fringe, (updated_cost_function, next_value_fringe))

    return False





# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))


    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])



