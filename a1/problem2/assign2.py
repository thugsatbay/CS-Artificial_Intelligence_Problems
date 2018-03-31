#!/usr/bin/env python
# Larry Gates
# Gurleen Dhody
# 15/Sept/2017

'''
RESULTS: withSmallestWork
-----------------------------------------
10-776 (12 secs) around 750-800
15-Best 1011 (14 secs) around 1000-1100
20-Best 1376 (33 secs) around 1350 - 1500
50-Best 3576 (95 secs) around 3500 - 3700
-----------------------------------------
'''

'''
RESULTS: localSearch
-----------------------------------------
10-723 (0.05 secs)
15-1075 (0.1 secs)
20-1304 (0.3 secs)
50-3163 (28 secs)
-----------------------------------------
'''

import random
import sys
import copy

class HashCode:
    def __init__(self):
        self.hash = {}
        self.hash_index = 0

    def hashStudent(self, name):
        self.hash[self.hash_index] = name
        self.hash_index += 1
        return self.hash_index-1

    def returnHashTable(self):
        return self.hash

class Student:
    def __init__(self, name):
        self.name = name
        self.star = []
        self.veto = []
        self.size = 0

    def checkMembershipInStarTeam(self, team):
        penalty = len(self.star)
        for each_star_member in self.star:
            if each_star_member in team:
                penalty -= 1
        return penalty

    def checkMembershipInVetoTeam(self, team):
        penalty = 0
        for each_veto_member in self.veto:
            if each_veto_member in team:
                penalty += 1
        return penalty

    def checkTeamSize(self, actual_team_size):
        if self.size:
            return not self.size == actual_team_size
        return 0
    
    def getName(self):
        return self.name

    def getRequestedTeamSize(self):
        return self.size

    def setRequestedTeamSize(self, t_size):
        self.size = t_size

    def setStarTeamMates(self, team):
        self.star = team

    def setVetoTeamMates(self, team):
        self.veto = team

    def getStarTeamMates(self):
        return self.star

    def getVetoTeamMates(self):
        return self.veto

class ReduceCourseStaffWorkload:
    def __init__(self, k=160, m=31, n=10):
        self.hash_names = HashCode()
        self.dic_student_objects = {}
        self.k, self.m, self.n = k, m, n

        self.single_member_teams = []
        self.double_member_teams = []
        self.triple_member_teams = []
        self.all_possible_teams = []
        self.len_all_possible_teams = 0

        self.minCost = float('inf')
        self.minCostState = []
        self.unique_members = 0

    def findAllPossibleTeamCombinations(self, all_players):
        #all_players = [player[1] for player in self.dic_student_objects.items()]

        # 1 Combo
        self.single_member_teams = [(self.findCostOfSingleTeam( [player_id] ), \
            [player_id]) for player_id in all_players]

        # 2 Combo
        self.double_member_teams = [ (self.findCostOfSingleTeam( \
            [player_id, second_player_id] ), [player_id, second_player_id]) \
            for index_one, player_id in enumerate(all_players) \
            for index_two, second_player_id in enumerate(all_players) \
            if index_one < index_two]

        # 3 Combo
        self.triple_member_teams = [ (self.findCostOfSingleTeam( \
            [player_id, second_player_id, third_player_id] ), \
            [player_id, second_player_id, third_player_id]) \
            for index_one, player_id in enumerate(all_players) \
            for index_two, second_player_id in enumerate(all_players) \
            for index_three, third_player_id in enumerate(all_players) \
            if index_one < index_two and index_two < index_three]

        self.single_member_teams = self.userFriendlyResult( \
            self.single_member_teams)
        self.double_member_teams = self.userFriendlyResult( \
            self.double_member_teams)
        self.triple_member_teams = self.userFriendlyResult( \
            self.triple_member_teams)

        self.all_possible_teams = self.single_member_teams + \
                                  self.double_member_teams + \
                                  self.triple_member_teams

        self.len_all_possible_teams = len(self.all_possible_teams)
    
    def findCostOfSingleTeam(self, team):
        team_cost = 0
        for each_student in team:
            # Cost for not getting the requested student.
            team_cost += each_student[1].checkMembershipInStarTeam(team) \
                * self.n
            # Cost for getting a student that was not asked for.
            team_cost += each_student[1].checkMembershipInVetoTeam(team) \
                * self.m

            # Check requested team size penalty.
            team_cost += each_student[1].checkTeamSize(len(team))
        return team_cost

    def findMinimumCost(self, state, index_space, players_left):
        # All players added.
        if players_left == 0:
            if state[0] < self.minCost:
                self.minCost = state[0]
                self.minCostState = state[1][:]
            return
        
        # All teams explored.
        if index_space == self.len_all_possible_teams:
            return

        if players_left - len(self.all_possible_teams[index_space]) < 0:
            return

        for index, probable_team in \
                            enumerate(self.all_possible_teams[index_space:]):
            
            # No team member can be in two teams, check for it.
            no_repetition = True
            for members in probable_team[1]:
                #print probable_team, "YOLO",state
                for each_team in state[1]:
                    if members in each_team[1]:
                        no_repetition = False
                        break
                if not no_repetition:
                    break
            if not no_repetition:
                continue

            # Backtracking to fit a team in given state
            # Add a team only if the cost is still less than the minCost found

            
            if state[0] + self.k + probable_team[0] < self.minCost:
                
                # Backtracking statements
                state[0] += self.k + probable_team[0]
                state[1].append(probable_team)
                self.findMinimumCost(state, index + 1, \
                                        players_left - len(probable_team[1]))
                state[0] -= (self.k + probable_team[0])
                state[1].pop()

    def getMinimumCostTeamState(self):
        for each_team in self.minCostState:
            print " ".join(each_team[1])
        print self.minCost
    
    def getUniqueMembersCount(self):
        return self.unique_members
    
    def printHashToNames(self):
        for key in self.dic_student_objects:
            print key, self.dic_student_objects[key][0]

    def userFriendlyResult(self, result, user=True):
        if user:
            return [(team[0], [each_player[1].getName() \
                for each_player in team[1]]) for team in result]
        return [(team[0], [each_player[0] \
            for each_player in team[1]]) for team in result]
            
    def readSurveyFile(self, filename):
        # Get all unique members.
        with open(filename, 'r') as f:
            for line in f:
                student_name = line.split(' ')[0]
                self.dic_student_objects[student_name] = (
                                self.hash_names.hashStudent(student_name), 
                                Student(student_name) )
        
        self.unique_members = len(self.dic_student_objects)
        # Get survey information of each player.
        with open(filename, 'r') as f:
            for line in f:
                student_team_info = line.split(' ')
                student_name = student_team_info[0]
                student_team_size = int(student_team_info[1])
                student_star, student_veto = [ele.strip() \
                    for ele in student_team_info[2:]]
                
                # Each survey line.
                if student_team_size:
                    self.dic_student_objects[student_name][1] \
                        .setRequestedTeamSize(student_team_size)
                if student_star != '_':
                    # List of all members that are requested.
                    team_obj = [self.dic_student_objects[each_name] \
                        for each_name in student_star.split(',')]
                    
                    # Add the list to the student object.
                    self.dic_student_objects[student_name][1] \
                        .setStarTeamMates(team_obj)
                if student_veto != '_':
                    # List of all members that are not requested.
                    team_obj = [self.dic_student_objects[each_name] \
                        for each_name in student_veto.split(',')]
                    
                    # Add the list to the student object.
                    self.dic_student_objects[student_name][1] \
                        .setVetoTeamMates(team_obj)

    def localSearch(self):
        all_people = sorted([[val[1]] for val in self.dic_student_objects.items()], key=lambda x : x[0])
        count = 0

        fmincost = float('inf')
        f_state = []
        # If no new states formed exit
        while True:
            state = []
            for each_team in all_people:
                state.append( (self.findCostOfSingleTeam(each_team), each_team) )
            # find cost of each team in state
            state = sorted(state, key=lambda x : x[0])
            
            # find max cost of team and try to remove it by joining with other teams to generate new states
            new_states = []
            for mv in xrange(len(state)-1, -1, -1):
                new_states = []
                same_cost = [state[mv]]
                max_index_in_state = [mv]
                # find duplicates of max team
                for max_index, each_team in enumerate(state[:-1]):
                    if each_team[0] == state[-1][0]:
                        same_cost.append(each_team)
                        max_index_in_state.append(max_index)
                
                for max_index, max_cost_state in enumerate(same_cost):
                    for index, each_team in enumerate(state):
                        # two teams can join to reduce cost based they are not same and the team size is less than 4
                        if index != max_index_in_state[max_index] and (len(each_team[1]) + len(max_cost_state[1])) <= 3:
                            new_state = copy.deepcopy(state)
                            # delete the teams that will be joined
                            del new_state[max(max_index_in_state[max_index], index)]
                            del new_state[min(max_index_in_state[max_index], index)]
                            new_state = [ele[1] for ele in new_state]
                            new_state.append(max_cost_state[1] + each_team[1])
                            new_states.append(new_state)

                #  if new states found exit
                if len(new_states):
                    break

            # if no new states found cant search further
            if not len(new_states):
                break

            # find cost of each state
            new_states_cost = []
            for stat in new_states:
                cost_per_state = 0
                for team in stat:
                    cost_per_state += self.findCostOfSingleTeam(team)
                cost_per_state += len(stat) * self.k
                new_states_cost.append((cost_per_state, stat))

            # sort the states based on cost
            new_states_cost = sorted(new_states_cost, key = lambda x: x[0])
            all_people = new_states_cost[0][1]
            count += 1
            # if a result found of state is global min store it
            if fmincost > new_states_cost[0][0]:
                fmincost = new_states_cost[0][0]
                f_state = all_people

        # print the final result
        for team in f_state:
            print " ".join( [mem[1].getName() for mem in team])
        print fmincost


    def withSmallestWork(self):
        global_cost = float('inf')
        global_path =[]
        for _ in xrange(10):
            totalCost = 0
            teams = []
            all_people = sorted([val[1] for val in self.dic_student_objects.items()], key=lambda x : x[0])
            random.shuffle(all_people)
            while len(all_people):
                new_9_state = {}
                explore = []
                # Add one person at a time who are remaining, if list exhausted of explore
                for new_person in all_people:
                    # should not already be searched
                    if new_person not in new_9_state:
                        
                        # Ready to explore based on new person graph
                        explore.append(new_person)
                        # create a heuristic for each person, where n is a +ve 
                        # cost he/she is favoured and should be in the state 
                        # space negative is m he/she is not desired for the given 
                        # state. Then pick the top 9 those who have a high favourable
                        # factor and make teams from them.
                        while len(explore):
                            each_person = explore.pop(0)
                            if each_person in new_9_state:
                                new_9_state[each_person] += 0
                            else:
                                new_9_state[each_person] = 0
                            
                            # like
                            for each_star in each_person[1].getStarTeamMates():
                                if each_star in all_people:
                                    if each_star in new_9_state:
                                        new_9_state[each_star] += self.n
                                    else:
                                        explore.append(each_star)
                                        new_9_state[each_star] = self.n
                            
                            # hate
                            for each_veto in each_person[1].getVetoTeamMates():
                                if each_veto in all_people:
                                    if each_veto in new_9_state:
                                        new_9_state[each_veto] -= self.m
                                    else:
                                        new_9_state[each_veto] = -self.m
                
                # Top 9 m,n heuristic
                store = sorted(new_9_state.items(), key=lambda x : x[1])
                # Get best 9 cost players
                if len(store) >= 9:
                    store = store[-9:]

                # Find the solution for these 9 players
                store = map(lambda x : x[0], store)
                self.findAllPossibleTeamCombinations(store)
                self.findMinimumCost(state=[0, []], index_space=0, \
                    players_left=len(store))
                
                # Store result for given 9 team
                if len(store) != 1:
                    for each_team_in_result in self.minCostState:
                        teams.append(each_team_in_result)
                    totalCost += self.minCost
                else:
                    totalCost += self.all_possible_teams[0][0] + self.k
                    teams.append(self.all_possible_teams[0])

                #self.getMinimumCostTeamState()

                # Reset the cost metric
                self.minCost = float('inf')
                self.minCostState = []
                
                # Remove the players that have been assigned to teams in local search space
                for each_player_done in store:
                    all_people.remove(each_player_done)
            
            # concatenated results stored in class variables
            if totalCost < global_cost:
                global_cost = totalCost
                global_path = teams
            self.minCost = global_cost
            self.minCostState = global_path
            #print teams
        self.getMinimumCostTeamState()


if not len(sys.argv) == 5:
    print("Not enough arguments provided")
    exit()
fileName = sys.argv[1]
k, m, n = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
findTeams = ReduceCourseStaffWorkload()
findTeams.readSurveyFile(filename=fileName)
#findTeams.withSmallestWork()
findTeams.localSearch()
