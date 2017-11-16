# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print 'successorGameState \n', successorGameState
        # print 'newPos', newPos
        # print 'newFood \n', newFood
        # print 'newGhostStates[0]', newGhostStates[0]
        # print 'newScaredTimes', newScaredTimes

        score = successorGameState.getScore()

        newGhostPos = newGhostStates[0].getPosition()
        G_dist = manhattanDistance(newPos, newGhostPos)

        newFoodPos = newFood.asList()
        F_dist = [manhattanDistance(newPos, x) for x in newFoodPos]

        # Ghost distance matters us most, so let's decrease score by higher Rate
        # in comparision to its increase with proximity with food
        # (g_rate, f_rate)
        # (4, 2.5) => score = 1158.2
        # (8, 6.5) => score = 1187.5
        g_rate = 8
        if G_dist > 0:
            score = score - g_rate/G_dist

        f_rate = 6.5
        if F_dist:
            nearestF_dist = min(F_dist)
            score = score + f_rate/nearestF_dist
            # added number of food left
            score = score - 2/len(newFoodPos)

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def isPacman(self, gameState, agent):
        return agent % gameState.getNumAgents() == 0

    def isTerminal(self, gameState, depth, agent):
        return gameState.isWin() or gameState.isLose() or depth == self.depth or gameState.getLegalActions(agent) == 0
        # return True

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # print 'gameState.getLegalActions(0)', gameState.getLegalActions(0)
        # print 'gameState.getNumAgents() ', gameState.getNumAgents()
        # util.raiseNotDefined()
        # list of actions starting at 0 i.e pacman
        # eg. result can be ['Left', 'Center', 'Right']
        lActions = gameState.getLegalActions(0)

        # check for all directions which can fetch maximum value
        mydict= {}
        for a in lActions:
            v = self.minimax(gameState.generateSuccessor(0, a), 0, 1)
            mydict[a] = v
        return max(mydict, key=mydict.get)

    def minimax(self, gameState, depth, agent):
        # RuntimeError: maximum recursion depth exceeded
        # if self.isPacman(gameState, agent):
        #     return self.minimax(gameState, depth+1, 0)
        if agent == gameState.getNumAgents():
            return self.minimax(gameState, depth+1, 0)

        if self.isTerminal(gameState, depth, agent):
            return self.evaluationFunction(gameState)

        # successors = []
        # lActions = gameState.getLegalActions(agent)
        # for a in lActions:
        #     v = self.minimax(gameState.generateSuccessor(agent, a), depth, agent+1)
        #     successors.append(v)
        #
        # return min(successors) if self.isPacman(gameState, agent) else max(successors)
        successors = (
                self.minimax(gameState.generateSuccessor(agent, action), depth, agent + 1)
                for action in gameState.getLegalActions(agent)
            )
        if self.isPacman(gameState, agent):
            maxv = max(successors)
        else:
            maxv = min(successors)
        return maxv


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        s,action = self.findfunc(gameState, 0, 0)
        return action

    def evaluate(self, state, depth, agent, alpha, beta, score, flag):
        bestAction = None
        bestScore = score

        lActions = state.getLegalActions(agent)
        for action in lActions:
            successor = state.generateSuccessor(agent, action)
            score, a = self.findfunc(successor, depth, agent + 1, alpha, beta)
            if flag == True:
                bestScore, bestAction = max((bestScore, bestAction), (score, action))
            else:
                bestScore, bestAction = min((bestScore, bestAction), (score, action))

            if not self.isPacman(state, agent):
                if bestScore < alpha:
                    return bestScore, bestAction
                beta = min(beta, bestScore)
            else:
                if bestScore > beta:
                    return bestScore, bestAction
                alpha = max(alpha, bestScore)

        return bestScore, bestAction

    def findfunc(self, gameState, depth, agent, alpha= float("-inf"), beta= float("inf")):
        if agent == gameState.getNumAgents():
            agent = 0
            depth += 1

        if self.isTerminal(gameState, depth, agent):
            return self.evaluationFunction(gameState), None

        isPac = self.isPacman(gameState, agent)

        if not isPac:
            return self.evaluate(gameState, depth, agent, alpha, beta, float('inf'), False)
        else:
            return self.evaluate(gameState, depth, agent, alpha, beta, float('-inf'), True)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
