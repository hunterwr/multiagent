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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        currPos = currentGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        ghostState = successorGameState.getGhostStates()
        currghostDist = []
        succghostDist = []
        closestsuccGhost = 0
        closestcurrGhost = 0
        for ghost in ghostState:
            ghostPos = ghost.getPosition()
            succghostDist.append(util.manhattanDistance(newPos, ghostPos))
            currghostDist.append(util.manhattanDistance(currPos, ghostPos))
        if len(currghostDist) > 0:
            closestsuccGhost = min(succghostDist)
            closestcurrGhost = min(currghostDist)
        if newScaredTimes[0] == 0:
            if closestsuccGhost < closestcurrGhost:
                score = score - 2
            elif closestsuccGhost == closestcurrGhost:
                score = score - 1
        if newScaredTimes[0] >= 1:
            if closestcurrGhost == 0:
                score = score + 5
            else:
                score = score + 1

        foodList = newFood.asList()
        succfoodDist = []
        currfoodDist = []
        closestcurrFood = 0
        closestsuccFood = 0
        for food in foodList:
            currfoodDist.append(util.manhattanDistance(currPos, food))
            succfoodDist.append(util.manhattanDistance(newPos, food))
        if len(currfoodDist) > 0:
            closestsuccFood = min(succfoodDist)
            closestcurrFood = min(currfoodDist)
        if closestsuccFood < closestcurrFood:
            score = score + 5
        elif closestsuccFood >= closestcurrFood:
            score = score - 1

        if newPos == ghostState[0].getPosition():
            score = score - 5

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actionDic = {}
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = self.min_value(successor, 1, 1)
            actionDic[action] = value
        return max(actionDic, key=lambda key: actionDic[key])

    def max_value(self, gameState, depth, agent):
        value_max = -10000
        if depth == self.depth or len(gameState.getLegalActions(agent)) == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            value_max = max(value_max, self.min_value(successor, depth + 1, agent + 1))
        return value_max

    def min_value(self, gameState, depth, agent):
        value_min = 10000
        if len(gameState.getLegalActions(agent)) == 0:
            return self.evaluationFunction(gameState)
        if agent == gameState.getNumAgents() - 1:
            for action in gameState.getLegalActions(agent):
                successor = gameState.generateSuccessor(agent, action)
                value_min = min(value_min, self.max_value(successor, depth, 0))
        else:
            for action in gameState.getLegalActions(agent):
                successor = gameState.generateSuccessor(agent, action)
                value_min = min(value_min, self.min_value(successor, depth, agent + 1))
        return value_min

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = -float("inf")
        beta = float("inf")
        value, action = self.max_value(gameState, 0, 0, alpha, beta)
            
        return action

    def max_value(self, gameState, depth, agent, alpha, beta):
        value_max = float('-inf')
        best_action = None
        if depth == self.depth or len(gameState.getLegalActions(agent)) == 0:
            return self.evaluationFunction(gameState), best_action
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            value_max_2, _ = self.min_value(successor, depth + 1, agent + 1, alpha, beta)
            print(f"v: {value_max}, v2: {value_max_2}")
            if value_max_2 > value_max:
                value_max = value_max_2
                alpha = max(alpha, value_max)
                best_action = action
            if value_max > beta:
                print("Pruned")
                return value_max, best_action
        return value_max, best_action

    def min_value(self, gameState, depth, agent, alpha, beta):
        value_min = float("inf")
        best_action = None
        if len(gameState.getLegalActions(agent)) == 0:
            return self.evaluationFunction(gameState), best_action
        if agent == gameState.getNumAgents() - 1:
            for action in gameState.getLegalActions(agent):
                successor = gameState.generateSuccessor(agent, action)
                value_min_2, _ = self.max_value(successor, depth, 0, alpha, beta)
                print(f"v: {value_min}, v2: {value_min_2}")
                if value_min_2 < value_min:
                    value_min = value_min_2
                    beta = min(beta, value_min)
                    best_action = action
                if value_min < alpha:
                    print("Pruned")
                    return value_min, best_action
        else:
            for action in gameState.getLegalActions(agent):
                successor = gameState.generateSuccessor(agent, action)
                value_min_2, _ = self.min_value(successor, depth, agent + 1, alpha, beta)
                print(f"v: {value_min}, v2: {value_min_2}")
                if value_min_2 < value_min:
                    value_min = value_min_2
                    beta = min(beta, value_min)
                    best_action = action
                if value_min < alpha:
                    print("Pruned")
                    return value_min, best_action
        return value_min, best_action


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
        _, action = self.max_value(gameState, 0, 0)
        return action

    def max_value(self, gameState, depth, agent):
        if depth == self.depth or len(gameState.getLegalActions(agent)) == 0:
            return self.evaluationFunction(gameState), None

        value_max = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            value_max_2, _ = self.exp_value(successor, depth, agent + 1)
            if value_max_2 > value_max:
                value_max = value_max_2
                best_action = action

        return value_max, best_action

    def exp_value(self, gameState, depth, agent):
        if len(gameState.getLegalActions(agent)) == 0:
            return self.evaluationFunction(gameState), None

        value_exp = 0
        actions = gameState.getLegalActions(agent)

        for action in actions:
            successor = gameState.generateSuccessor(agent, action)
            if agent == gameState.getNumAgents() - 1:
                value_exp += self.max_value(successor, depth + 1, 0)[0]
            else:
                value_exp += self.exp_value(successor, depth, agent + 1)[0]

        average_value = value_exp / len(actions)
        return average_value, None

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    currPos = currentGameState.getPacmanPosition()
    ghostPos = currentGameState.getGhostStates()
    ghostPos = ghostPos[0].getPosition()
    foodList = currentGameState.getFood().asList()
    foodDist = []
    for food in foodList:
        foodDist.append(util.manhattanDistance(currPos, food))
    if len(foodDist) == 0:
        closestFood = 1
    else:
        closestFood = min(foodDist)

    #print(f"Closest food: {closestFood})
    ghost_dist = util.manhattanDistance(currPos, ghostPos)


    pacman_state = currentGameState.getPacmanState()
    pacman_action = pacman_state.configuration.direction


    if ghost_dist >= 7:
        move_randomly = random.random()
        if move_randomly <= 0.10:  # Adjust the threshold as needed
            return 10
        return 1 / closestFood

    else:
        # Adjust the weight based on ghost proximity
        
        return ghost_dist + 1 / closestFood

    # currPos = currentGameState.getPacmanPosition()
    # ghostState = currentGameState.getGhostStates()
    # ghostPos = ghostState[0].getPosition()
    # foodList = currentGameState.getFood().asList()
    # foodDist = []
    # for food in foodList:
    #     foodDist.append(util.manhattanDistance(currPos, food))
    # if len(foodDist) == 0:
    #     closestFood = 1
    # else:
    #     closestFood = min(foodDist)
    # ghostDist = util.manhattanDistance(currPos, ghostPos)
    # if ghostDist >= 8:
    #     return ghostDist
    # elif 8 > ghostDist >= 5:
    #     return ghostDist + 0.25 / closestFood
    # elif 5 > ghostDist >= 2:
    #     return ghostDist + 0.5 / closestFood
    # return ghostDist + 1 / closestFood

# Abbreviation
better = betterEvaluationFunction
