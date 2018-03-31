#!/usr/bin/env python
# Gurleen Dhody
# Larry Gates
# 15/Sept/2017

'''
(1) Which search algorithm seems to work best for each routing options? 
-Astar is both good computationally and memory wise. Plus it tries to expand 
towards goal state faster.

--------------------------------------------------------------------------------

(2) Which algorithm is fastest in terms of the amount of computation time 
required by your program, and by how much, according to your experiments? 
-Astar is 7.6 times faster than uniform. Uniform is considered the second 
fastest. We have not included dfs for comparison as it will always provide a 
greedy solution which is very poor.

--------------------------------------------------------------------------------

(3) Which algorithm requires the least memory, and by how much, according 
to your experiments? 
-DFS requires the least space since a globally visited node is enough
to keep track of cities visited and current route.
-Uniform and Astar both require an implementation of priority queue. So at any
given state it will have information about max n city states. Where n being the
total cities.

--------------------------------------------------------------------------------

(4) Which heuristic function(s) did you use, how good is it, and how might 
you make it/them better?
-We used the eculidian distance. The problem is that since some cities don't 
have coordinate systems, gps location. This causes sometimes the astar to
faulter and give poorer results compared to uniform. Still it will give
the closest optimum. This happens because of our assumption of handling
the missing gps information. For cities having no gps location heuristic
function returns infinity cost. In this case we add our city to the priority
queue with a cost just to travel the path, keeping heuristic cost to 0.

--------------------------------------------------------------------------------

ASSUMPTIONS:
Default values assumed if no data provided. Found using running stats.py
Basically it is the average miles and speed of all cities that have complete 
data.
miles = 24.24
speed = 49.00
GPS coordinates = infinity if not given
'''

from heapq import heappush, heappop
from math import sqrt
import Queue as Q
import sys
sys.setrecursionlimit(20000)
'''
heappop - pop and return the smallest element from heap
heappush - push the value item onto the heap, maintaining heap invarient
'''

class MinHeap:
    '''
    A class for Min Heap naive O(n) insertion and O(nlogn) extraction, 
    helps with optimization though
    '''
    # Constructor to initialize a heap
    def __init__(self, first_key):
        self.heap = []
        self.key_value = {}
        self.insertKey(first_key)

    # Method to remove minium element from min heap
    def extractMin(self):
        # Sort the heap and return the first element
        self.heap = sorted(self.heap, key = lambda x : x[0])
        element_to_return, self.heap = self.heap[0], self.heap[1:]
        return element_to_return[1]

    # Inserts a new key and value 'k'
    def insertKey(self, k):
        # state = (distance, time, step_cost, my_route, visited, current_city)
        # ele = [[cost, state]]
        for ele in self.heap:
            # Find if city already in the heap
            if ele[1][4].getCity() == k[1][4].getCity():
                # If city already there keep one with minimum cost
                if ele[0] > k[0]:
                    ele[0] = k[0]
                    ele[1] = k[1]
                return
        # If city not found add it to the heap
        self.heap.append(k)

    def lengthOfHeap(self):
        return len(self.heap)

class StateCode:
    '''Helper class to encode state name to integer hash'''
    def __init__(self):
        self.state_name_table = {}
        self.hash_to_state_name = {}
        self.hash = 0

    def getHash(self,
                state_name):
        if state_name in self.state_name_table:
            return self.state_name_table[state_name]
        self.state_name_table[state_name] = state_name
        self.hash_to_state_name[state_name] = state_name
        self.hash += 1
        return (self.hash-1)

    def returnHashToStateName(self,
                              hash_code):
        return self.hash_to_state_name[hash_code]

class RouteInformation:
    '''Route Information'''
    def __init__(self,
                 miles,
                 speed):
        # Averge default parameters - refer stats.py
        self.miles = 24.24
        self.speed = 49.00
        self.time = 0.0
        if miles is not None and not miles == "":
            self.miles = float(miles)
        if speed is not None and not speed == "":
            self.speed = float(speed)
        # If distance is 0, data wrong time = miles
        if self.speed != float(0):
            self.time = float(self.miles / self.speed)
        else:
            self.time = self.miles

    def getMiles(self):
        return self.miles

    def getSpeed(self):
        return self.speed

    def getTime(self):
        return self.time

class City:
    '''Store City Information'''
    def __init__(self,
                 city_details,
                 latitude,
                 longitude):
        self.city = city_details
        self.lat = latitude
        self.long = longitude
        self.connections = {}

    def getCity(self):
        return self.city

    def getLatitude(self):
        return self.lat

    def getLongitude(self):
        return self.long

    def getConnections(self):
        return self.connections

    def connectTo(self,
                  destination,
                  highway,
                  route_info=None,
                  new_city=None):
        '''
        Connects to another City object where destination and highway act 
        as the key
        '''
        self.connections[(destination, highway)] = [route_info, new_city]

class CityHunter:    
    def __init__(self,
                 routing_algo=None,
                 cost_func=None,
                 heuristic='eculidian'):
        '''Input Initializer'''
        # Constant definitions
        self.COST_FUNCTIONS = ('segments', 'distance', 'time')
        self.ROUTING_ALGOS = ('bfs', 'uniform', 'dfs', 'astar')
        self.HEURISTIC_FUNCTIONS = ('eculidian', )
        self.GPS_FILE = './city-gps.txt'
        self.ROAD_FILE = './road-segments.txt'
        
        # State Hash Initializer
        self.state_code = StateCode()

        # Default Initialization
        self.cost = float('inf')
        self.total_distance = 0.0
        self.total_time = 0.0
        self.route_path = []
        self.routing_algorithm = routing_algo
        self.cost_function = cost_func
        self.heuristic_type = heuristic
        self.end_city_obj = None
        
        # Graph Map
        self.node_jump = {}

    def astar(self, state_space_start):        
        abc=True
        state_space = Q.PriorityQueue()
        state_space.put(state_space_start)
        visited = {}
        while not state_space.empty():
            current_node = state_space.get()
            distance, time, step_cost, my_route, current_city = current_node[1]

            # Path already explored, this route had more cost hence bad path
            if current_city.getCity() in visited:
                continue

            # If city found return with answer.
            if current_city.getCity() == self.end_city:
                self.total_distance, self.total_time, self.route_path = \
                    distance, time, my_route
                self.cost = step_cost
                return True
            
            routes_for_current_city = current_city.getConnections()
            visited[current_city.getCity()] = 1
            # Expanding all routes of a city.
            for each_route in routes_for_current_city:
                route_info, target_city = routes_for_current_city[each_route]

                potential_heuristic_distance = \
                            self.heuristic(target_city, self.end_city_obj)

                if target_city.getCity() in visited:
                    continue
             
                p_distance = distance + route_info.getMiles()
                p_time = time + route_info.getTime()
                p_step_cost = step_cost + self.costFunction(route_info)
                
                
                if potential_heuristic_distance == float('inf'):
                    state_space.put( (p_step_cost, [ \
                                    p_distance, \
                                    p_time, \
                                    p_step_cost, \
                                    my_route + [target_city.getCity()], \
                                    target_city]) )
                else:
                    state_space.put( (p_step_cost + potential_heuristic_distance,
                                    [   p_distance, \
                                        p_time, \
                                        p_step_cost, \
                                        my_route + [target_city.getCity()], \
                                        target_city ])  )
        return False

    def bfs(self, state_space):
        new_state_space = []
        # Expand over all state spaces at given depth, keep one entry per city,
        # based on minimum distance.
        efficiency_dic = {}
        for each_state in state_space:
            # Keep city with minimum metric of cost function
            if each_state[5].getCity() in efficiency_dic and \
                    efficiency_dic[each_state[5].getCity()][0] > each_state[2]:
                efficiency_dic[each_state[5].getCity()] = \
                                                    (each_state[2], each_state)
            elif each_state[5].getCity() not in efficiency_dic:
                efficiency_dic[each_state[5].getCity()] = \
                                                    (each_state[2], each_state)
        state_space = [efficiency_dic[key][1] for key in efficiency_dic.keys()]
        while len(state_space):
            # Expand the details and variables of that state space.
            distance, time, step_cost, my_route, visited, current_city = \
                                                            state_space.pop(0)
            if self.end_city == current_city.getCity():
                if step_cost < self.cost:
                    self.total_distance, self.total_time, self.route_path = \
                                                    distance, time, my_route
                    self.cost = step_cost
                    # Exit once you have found a result, can continue to find 
                    # best solution
                    return True
            # If no city matched end city, generate new state spaces at d+1 
            # depth to explore.
            current_city_routes = current_city.getConnections()
            route_info, updated_cost, dest_city_node = None, None, None
            # For global visited state space, currently maintaining a local 
            # state space
            # Gives better results
            # visited.append(current_city.getCity())
            for route in current_city_routes.keys():
                # The current_city_routes dictonary stores route information at
                # 0 and next city at index 1 for given key.
                route_info = current_city_routes[route][0]
                updated_cost = step_cost + self.costFunction(route_info)
                if route[0] not in visited and updated_cost < self.cost:
                    dest_city_node = current_city_routes[route][1]
                    new_state_space.append([
                                        distance + route_info.getMiles(),
                                        time + route_info.getTime(),
                                        updated_cost,
                                        my_route + [dest_city_node.getCity()],
                                        visited + [current_city.getCity()],
                                        dest_city_node ])
        # If no new state space found means complete graph explored quit search.
        if not len(new_state_space):
            if self.cost != float('inf'):
                return True
            return False
        return self.bfs(new_state_space)

    def costFunction(self, route_info):
        # segments
        if self.cost_function ==  self.COST_FUNCTIONS[0]:
            return 1
        # distance 
        if self.cost_function ==  self.COST_FUNCTIONS[1]:
            return route_info.getMiles()
        # time
        return route_info.getTime()

    def decodeCityName(self,
                    city_tuple):
        '''Decode state name to a string using hashcode'''
        return self.state_code.returnHashToStateName(hash)

    def dfs(self, distance, time, step_cost, my_route, visited, current_city):
        if self.end_city == current_city.getCity():
            if step_cost < self.cost:
                self.total_distance, self.total_time, self.route_path = \
                                                    distance, time, my_route
                self.cost = step_cost
            return True
        if step_cost > self.cost:
            return False
        # If city does not matches end city, generate all state spaces at 
        # and keep on exploring.
        current_city_routes = current_city.getConnections()
        route_info, updated_cost, dest_city_node = None, None, None
        search_status = False
        visited.append(current_city.getCity())
        for route in current_city_routes.keys():
            # The current_city_routes dictonary stores route information at 0 
            # and next city at index 1 for given key.
            route_info = current_city_routes[route][0]
            updated_cost = step_cost + self.costFunction(route_info)
            if route[0] not in visited and updated_cost < self.cost:
                dest_city_node = current_city_routes[route][1]
                search_status = search_status or \
                                self.dfs(
                                        distance + route_info.getMiles(),
                                        time + route_info.getTime(),
                                        updated_cost,
                                        my_route + [dest_city_node.getCity()],
                                        visited, #+ [current_city.getCity()],
                                        dest_city_node)
        # If no new state space found means complete graph explored quit search.
        return search_status
    
    def encodeCityName(self,
                       city_data):
        '''Encode state name so to save space'''
        city_name, state = city_data.split(',_')
        state = self.state_code.getHash(state)
        return (city_name, state)

    def findPath(self):
        # bfs
        if self.routing_algorithm == self.ROUTING_ALGOS[0]:
            if self.bfs( \
                    [ [0.0, 0.0, 0.0, [], [], \
                    self.node_jump[self.start_city]] ] ):
                self.printResult()
                return
            print "No route exists to", self.end_city, " from", self.end_city
        # uniform
        elif self.routing_algorithm == self.ROUTING_ALGOS[1]:
            # Weight of branch, state_space_initial values list.
            min_heap_state_space = MinHeap(
                                            (0, [0.0, 0.0, 0.0, [], \
                                            self.node_jump[self.start_city]] )
                                          )
            if self.uniform(min_heap_state_space, []):
                self.printResult()
                return
            print "No route exists to", self.end_city, " from", self.end_city
        # dfs
        elif self.routing_algorithm == self.ROUTING_ALGOS[2]:
            if self.dfs(0.0, 0.0, 0.0, [], [], self.node_jump[self.start_city]):
                self.printResult()
                return
            print "No route exists to", self.end_city, " from", self.end_city
        # astar
        elif self.routing_algorithm == self.ROUTING_ALGOS[3]:
            if self.astar( \
                    ( 0.0, (0.0, 0.0, 0.0, [], self.node_jump[self.start_city])) ):
                self.printResult()
                # self.route_description()
                return
            print "No route exists to", self.end_city, " from", self.end_city

    def heuristic(self, source_city, target_city):
        if self.heuristic_type == self.HEURISTIC_FUNCTIONS[0]:
            return sqrt( \
                (source_city.getLatitude() - target_city.getLatitude())**2 + \
                (source_city.getLongitude() - target_city.getLongitude())**2)

    def printResult(self):
        print int(self.total_distance), self.total_time, \
            str(self.start_city[0] + ",_" + \
            self.state_code.returnHashToStateName(self.start_city[1])), \
            " ".join( map(lambda x : str(x[0] + ",_" + \
            self.state_code.returnHashToStateName(x[1])), self.route_path))

    def readDataFile(self):
        '''Read the data text files'''
        # Open gps text file.
        with open(self.GPS_FILE, 'r') as gps:
            for index, coordinate in enumerate(gps):
                line = coordinate.split(" ")
                city_block = self.encodeCityName(line[0])
                self.node_jump[city_block] = City( \
                                                    city_block, \
                                                    float(line[1]), \
                                                    float(line[2]))

        # Open roads text file.
        with open(self.ROAD_FILE, 'r') as segment:
            for index, road in enumerate(segment):
                line = road.split(" ")
                city_block = self.encodeCityName(line[0])
                city_dest = self.encodeCityName(line[1])
                # Store cities whose coordinates are not given.
                if city_block not in self.node_jump:
                    self.node_jump[city_block] = City( \
                                                        city_block, 
                                                        float('inf'), 
                                                        float('inf'))
                if city_dest not in self.node_jump:
                    self.node_jump[city_dest] = City( \
                                                        city_dest, 
                                                        float('inf'), 
                                                        float('inf'))
                # Bi-directional roads.
                self.node_jump[city_block].connectTo(city_dest, line[4], \
                    RouteInformation( line[2], line[3] ), \
                    self.node_jump[city_dest])
                self.node_jump[city_dest].connectTo(city_block, line[4], \
                    RouteInformation( line[2], line[3] ), \
                    self.node_jump[city_block])
    
    def route_description(self):
        route = [self.start_city] + self.route_path
        distance = 0
        for index, node in enumerate(route[:-1]):
            connections = self.node_jump[node].getConnections()
            for connect in connections.keys():
                if connections[connect][1].getCity() == route[index + 1]:
                    distance += connections[connect][0].getMiles()
                    print route[index], route[index + 1], \
                          connections[connect][0].getMiles(), \
                          connections[connect][0].getTime(), \
                          distance
        print distance

    def setEndCity(self,
                   end):
        self.end_city = self.encodeCityName(end)
        self.end_city_obj = self.node_jump[self.end_city]
    
    def setStartCity(self,
                     start):
        self.start_city = self.encodeCityName(start)

    def uniform(self, state_space, visited):
        # Expand the state space that has minimum weight edge.
        # Expand the details and variables of that state space.
        distance, time, step_cost, my_route, current_city = \
            state_space.extractMin()
        if self.end_city == current_city.getCity():
            if step_cost < self.cost:
                self.total_distance, self.total_time, self.route_path = \
                    distance, time, my_route
                self.cost = step_cost
        # If no city matched end city, generate new state spaces at d+1 depth 
        # to explore
        # Maintain a global visited state
        visited.append(current_city.getCity())
        current_city_routes = current_city.getConnections()
        for route in current_city_routes.keys():
            route_info = current_city_routes[route][0]
            updated_cost = step_cost + self.costFunction(route_info)
            if route[0] not in visited and updated_cost < self.cost:
                dest_city_node = current_city_routes[route][1]
                state_space.insertKey( [
                                    updated_cost, [
                                        distance + route_info.getMiles(),
                                        time + route_info.getTime(),
                                        updated_cost,
                                        my_route + [dest_city_node.getCity()],
                                        dest_city_node]
                                    ] )
        # If no new state space found means complete graph explored quit search.
        if not state_space.lengthOfHeap():
            if self.cost != float('inf'):
                return True
            return False
        return self.uniform(state_space, visited)

if not len(sys.argv) == 5:
    print("Not enough arguments")
else:
    call = CityHunter(
                    routing_algo=sys.argv[3],
                    cost_func=sys.argv[4])
    call.readDataFile()
    call.setStartCity(sys.argv[1])
    call.setEndCity(sys.argv[2])
    call.findPath()
#route.py Bloomington,_Indiana Indianapolis,_Indiana dfs distance
