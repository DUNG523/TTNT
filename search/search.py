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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # Initialize the stack to hold nodes to explore
    stack = util.Stack()

    # Initialize a set to keep track of visited nodes
    visited = set()

    # Push the start state onto the stack along with an empty list of actions
    stack.push((problem.getStartState(), []))

    # Continue searching until the stack is empty
    while not stack.isEmpty():
        # Pop the current state and the actions taken to reach this state
        current_state, actions = stack.pop()

        # If the current state is the goal state, return the list of actions
        if problem.isGoalState(current_state):
            return actions

        # Check if the current state has already been visited
        if current_state not in visited:
            # Mark the current state as visited
            visited.add(current_state)

            # Get the successors of the current state
            successors = problem.getSuccessors(current_state)

            # Push each successor onto the stack along with the actions taken to reach it
            for next_state, action, _ in successors:
                stack.push((next_state, actions + [action]))

    # If no solution is found, return an empty list
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    # Create a queue to store nodes to be explored
    frontier = util.Queue()

    # Initialize the frontier with the start state
    frontier.push((problem.getStartState(), []))

    # Create a set to keep track of explored states
    explored = set()

    # Start BFS
    while not frontier.isEmpty():
        # Get the current state and the actions taken to reach this state
        current_state, actions = frontier.pop()

        # Check if the current state is the goal state
        if problem.isGoalState(current_state):
            return actions

        # Check if the current state has already been explored
        if current_state not in explored:
            # Add the current state to the explored set
            explored.add(current_state)

            # Explore the successors of the current state
            for successor, action, _ in problem.getSuccessors(current_state):
                # Check if the successor state has already been explored or in the frontier
                if successor not in explored:
                    # Add the successor state and the actions to reach it to the frontier
                    frontier.push((successor, actions + [action]))

    # If no solution is found
    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # Initialize priority queue with start state and its cost
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), 0)  # (state, path, cost)

    # Initialize explored set
    explored = set()

    # Start searching
    while not frontier.isEmpty():
        current_state, current_path, current_cost = frontier.pop()

        # Check if current state is goal state
        if problem.isGoalState(current_state):
            return current_path

        # Check if current state is already explored
        if current_state not in explored:
            # Mark current state as explored
            explored.add(current_state)

            # Expand current state
            for successor, action, step_cost in problem.getSuccessors(current_state):
                # Calculate total cost for successor node
                total_cost = current_cost + step_cost
                # Add successor node to frontier
                frontier.push((successor, current_path + [action], total_cost), total_cost)

    return []  # Return empty path if no solution found


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Initialize the start state
    start_state = problem.getStartState()

    # Initialize the frontier using a priority queue
    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), 0)  # (state, actions, cost)

    # Initialize an empty set to keep track of explored states
    explored = set()

    # Start A* search
    while not frontier.isEmpty():
        # Pop the node from the frontier with the lowest priority
        current_state, actions, cost = frontier.pop()

        # Check if the current state is the goal state
        if problem.isGoalState(current_state):
            return actions

        # Check if the current state has been explored
        if current_state not in explored:
            # Mark the current state as explored
            explored.add(current_state)

            # Get successors of the current state
            successors = problem.getSuccessors(current_state)

            for successor, action, step_cost in successors:
                # Calculate the total cost from start to successor through current state
                total_cost = cost + step_cost

                # Calculate the priority (f(n) = g(n) + h(n))
                priority = total_cost + heuristic(successor, problem)

                # Add the successor to the frontier
                frontier.push((successor, actions + [action], total_cost), priority)

    # If no solution found
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
