# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# DFS, BFS, Uniform Search, A* all use this common search function
# myds:         data structure used
# visited:      keep track of visited nodes
# flag:         to discriminate between Stack, Queues, Priority Queues
# heuristic:    prevalent only in A*, for rest it's 0
def common_search(problem, myds, flag, heuristic):
    visited = set()
    # top = list(myds.pop())[0]
    while not myds.isEmpty():
        (node, cost, path) = myds.pop()

        # Return path if goal node is reached
        if problem.isGoalState(node):
            return path

        # if problem.getSuccessors(node):
        # if node is not visited, try expanding
        if not node in visited:
            visited.add(node)

            for c_node, c_path, c_cost in problem.getSuccessors(node):
                if not c_node in visited:
                    up_tuple = (c_node, cost + c_cost, path + [c_path])
                    # For DFS, BFS
                    if flag == 'sq':
                        myds.push(up_tuple)
                    # For Uniform Search & A*
                    elif flag == 'pq':
                        myds.push(up_tuple, cost + c_cost + heuristic(c_node, problem))
                    # result = common_search(problem, myds, visited)

# DFS, BFS, Uniform Search, A* all use this search_util function
# It initialises the function
# search_util and common_search can also be easily combined into one
def search_util(problem, myds, flag, heuristic):
    path = []
    cost = 0
    origin = problem.getStartState()
    origin_tuple = (origin, cost, path)
    # For Stacks and Queues
    if flag == 'sq':
        myds.push(origin_tuple)
    # For PriorityQueue
    # Heuristic in case of Uniform Search is simply 0
    # While in A* it will be passed as command-line arguments
    elif flag == 'pq':
        myds.push(origin_tuple, cost + heuristic(origin, problem))
    return common_search(problem, myds, flag, heuristic)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    # util.raiseNotDefined()
    myStack = util.Stack()
    flag = 'sq'
    heuristic = nullHeuristic

    return search_util(problem, myStack, flag, heuristic)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    myQueue = util.Queue()
    flag = 'sq'
    heuristic = nullHeuristic

    return search_util(problem, myQueue, flag, heuristic)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    myPriority_Queue = util.PriorityQueue()
    flag = 'pq'
    heuristic = nullHeuristic

    return search_util(problem, myPriority_Queue, flag, heuristic)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    myPriority_Queue = util.PriorityQueue()
    flag = 'pq'

    # return myPriority_Queue.push(origin_tuple, cost + heuristic(origin_tuple[0], problem))
    # return common_search(problem, myPriority_Queue, visited, flag, heuristic)
    return search_util(problem, myPriority_Queue, flag, heuristic)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
