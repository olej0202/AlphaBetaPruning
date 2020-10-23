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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

    def MAX_VALUE(self,state,depth ):
        if (self.depth == depth or state.isWin() or state.isLose()):#Løvnodene
            return self.evaluationFunction(state)
        v = int(-100000)
        for actions in state.getLegalActions(0):#ser på hver neste node i treet
            successorstate = state.generateSuccessor(0, actions)
            value = self.MIN_VALUE(successorstate, 1, depth)
            if value >= v:#Ser om verdien er mindre enn det man har
                v = value

        return v


    def MIN_VALUE(self,state, index, depth):
        if self.depth == depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        v=100000
        agent = index % (state.getNumAgents()-1)#Finner ut av hvilke agent som skal beveges neste gang
        if agent == 0:#Når det er siste spøkelse sin tur
            for actions in state.getLegalActions(index):
                sucsessorstate = state.generateSuccessor(index, actions)
                value=self.MAX_VALUE(sucsessorstate, depth+1)
                if value <= v:
                    v = value


        else:#Når det er neste spøkelse sin tur til å gjøre noe
            for actions in state.getLegalActions(agent):
                sucsessorstate = state.generateSuccessor(agent, actions)
                value=self.MIN_VALUE(sucsessorstate, index+1, depth)
                if value <= v:
                    v=value

        return v





    def getAction(self, gameState):
        # Går gjennom en runde for rot noden der hvert resultat legges til i en liste
        # Da resultatene blir lagt inn i samme rekkefølge som actions er i kan man se
        # på hvilken index som gir høyest verdi

        values=[]
        legalactions = gameState.getLegalActions(0)
        for actions in legalactions:
            status=gameState.generateSuccessor(0, actions)
            v = self.MIN_VALUE(status, 1, 0)
            values.append(v)
        i = values.index(max(values))

        return legalactions[i]






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        alpha=-100000
        beta=100000
        values=[]
        #Går gjennom en runde for rot noden der hvert resultat legges til i en liste
        #Da resultatene blir lagt inn i samme rekkefølge som actions er i kan man se
        #på hvilken index som gir høyest verdi
        legalactions = gameState.getLegalActions(0)
        for actions in legalactions:
            status=gameState.generateSuccessor(0, actions)
            v = self.MIN_VALUE(status, 0, 1, alpha, beta)
            values.append(v)
            alpha=max(alpha,v)
        i = values.index(max(values))

        return legalactions[i]


    def MAX_VALUE(self, state, depth, A, B):
        if self.depth == depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)#Løvnodene
        v=-100000
        alpha=A
        beta=B
        for actions in state.getLegalActions(0):
            successorstate = state.generateSuccessor(0, actions)
            value=self.MIN_VALUE(successorstate,depth, 1, alpha, beta)
            if value>=v:
                v=value
            if v>beta:#Ser når man kan prone
                return value
            alpha=max(alpha,v)#Oppdaterer alpha
        return v





    def MIN_VALUE(self, state, depth, index, A, B):
        if self.depth == depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        v=100000
        alpha=A
        beta=B
        agent = index % (state.getNumAgents() - 1)  # Finner ut av hvilke agent som skal beveges neste gang
        if agent == 0:  # Når det er siste spøkelse sin tur
            for actions in state.getLegalActions(index):
                sucsessorstate = state.generateSuccessor(index, actions)
                value = self.MAX_VALUE(sucsessorstate, depth + 1, alpha, beta)
                if value <= v:
                    v = value
                if v< alpha:#Når man kan prone
                    return v
                beta=min(beta,v)


        else:  # Når det er neste spøkelse sin tur til å gjøre noe
            for actions in state.getLegalActions(agent):
                sucsessorstate = state.generateSuccessor(agent, actions)
                value = self.MIN_VALUE(sucsessorstate,depth,index+1, alpha, beta )
                if value <= v:
                    v = value
                if v<alpha:
                    return v
                beta=min(beta,v)

        return v



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
