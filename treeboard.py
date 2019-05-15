import numpy as np
from anytree import NodeMixin, RenderTree
from anytree import Node, AsciiStyle
import random
import math
"""purpose of this class was to test if I could get objects placed as nodes
into the anytree python tree

you must install anytree with pip install in order to be able to run code

it seemed to have worked at least for constructing the nodes...
this class should be used to input into the treestructure, for MCTS purposes"""



class The_Base_Class(object):
    foo=4 #for testing ??

class Tree_Board_State(The_Base_Class, NodeMixin):
    x = 1
    o = -1
    #unoccupied square should be zero
    #board is numpy array 3x3 of integers
    #tictactoe is -1, or 1, or 0 for empty

    # I dont know if all nodeFeatures are necesary, but nodeParent and nodeChildren are probably required, to be implemented for the anytree API to work properly
    # API documentation is here at this link
    # https://anytree.readthedocs.io/en/latest/api/anytree.node.html#anytree.node.nodemixin.NodeMixin

    def __init__(self, the_state, whos_turn_it_is, state_value, the_visited_count, name, length, width, parent=None, children=None ):
        super(Tree_Board_State, self).__init__()
        self.board = the_state #initialize with numpy array 3x3, filled with zeroes
        self.current_turn = whos_turn_it_is #whos turn it is
        self.value = state_value
        self.visited_count = the_visited_count
        self.name = name
        self.length = length
        self.width = width
        self.parent = parent
        if children:
            self.children = children


    def __str__(self):
        return str(self.board) #print the goddam board

    def checkGameResult(self):
        #check if one player has won, or game continues
        b = self.board
        rowsum = np.sum(b, 0)
        colsum = np.sum(b, 1)
        diagsum1 = b[0,0] + b[1,1] + b[2,2]
        diagsum2 = b[0,2] + b[1,1] + b[2,0]

        if any(rowsum == 3) or any(colsum == 3) or (diagsum1 == 3) or (diagsum2 == 3):
            return 1 #gameresult1 AI wins
        elif any(rowsum == -3) or any(colsum == -3) or (diagsum1 == -3) or (diagsum2 == -3):
            return -1 #gameresult2 HumanPlayerWins
        elif np.all(b != 0):
            return 0 #draw was reached
        else:
            return 2 #game continues

    def isLegalMove(self ,newMarkerTuple):
        nr = newMarkerTuple[0] #row
        nc = newMarkerTuple[1] #col
        if self.board[nr, nc] == 0 and ((0 <= nr <= 3) and (0 <= nc <=3)): #check if newcoords is empty and newcoords are legalsize
            return True
        else:
            return False

    def makeLegalMove(self, newMarkerTuple): #parameter is the coords tuple like (0,1) for newPlayerMarker into board
        if self.isLegalMove(newMarkerTuple):
            newboard = self.board
            if self.current_turn == 0:
                marker = -1
                newturn = 1
            else:
                marker = 1
                newturn = 0
            newboard[newMarkerTuple[0], newMarkerTuple[1]] = marker
            #add the newboard into the gamertree, and switch turn
            New_Board_State = Tree_Board_State(newboard, newturn, 0, 0, name="newNode", length=0, width=0, parent=self, children=None )
            """return the newboardstate to the gaame treee, OR append the newNode to the currentNode (i.e. grow theGameTree)???"""
            return New_Board_State


    """I was tempted to make a switchTurnFunction
    but I decided not to... at least yet...
    in the realgame, the turns switch rather violently when mcts rootnode will be changed into the newGamestate 
    which means that the treeProgressesDownwards one depth at a time, after AI has done move, and after human has done a move
    
    but, it maybe necessary to do some kind of function so that I'm able to do turn switching in rollout phase nicely, and switch turns there, in simlation
    because... rollout phase will end up utilizing makeLegalMove function...
    in MCTSalgo class, the rollout phase will be defined for the most part..."""


    def switchTurn(self):
        if self.current_turn == 1:
            self.current_turn = 0
        elif self.current_turn == 0:
            self.current_turn = 1


    def getPlayerTurn(self):
        return self.current_turn

    def isLeafNode(self):
        res = True
        res = self.is_leaf
        return res

    def isRootNode(self):
        res = True
        res = self.is_root
        return res

    def expandCurrentNode(self, actionsList):
        originalboard = self.board.copy()
        if self.current_turn == 0:
            marker = -1
            newturn = 1
        else:
            marker = 1
            newturn = 0

        if len(actionsList) > 0:
            for act in actionsList:
                thenewboard = originalboard.copy()
                thenewboard[ act[0], act[1] ] = marker
                newNode = Tree_Board_State( thenewboard.copy(), newturn, 0, 0, name="expandedNode", length=0, width=0, parent=self,children=None )

    def getDirectChildNodes(self):
        #just get the childNodes as list, (instead of orignially tuple)
        temp = self.children
        if temp == None:
            return None
        lista = list(temp)
        return lista

    def getValue(self):
        return self.value

    def getVisited(self):
        return self.visited_count

    def incrementVisitedCount(self):
        self.visited_count += 1


    def getPossibleActions(self):
        #iterate the self.board to find where the empty squares are, and those are the possibleNewStates
        actionsList = []
        for r in range(3):
            for c in range(3):
                if self.board[r,c] == 0:
                    actionsList.append( (r,c) )

        couldNotExpandNodeTerminal = False
        if len(actionsList)==0:
            couldNotExpandNodeTerminal = True

        return actionsList, couldNotExpandNodeTerminal



    def getRandomAction(self):
        possibleActs, res = self.getPossibleActions()
        length = len(possibleActs)
        if length == 0:
            return None
        else:
            actInd = random.randint(0, length-1)
            return possibleActs[actInd]


    def getSingleUCB(self):
        n = self.getVisited()
        Vi = self.getValue()
        N = self.parent.getVisited()
        if n == 0:
            ucb = math.inf
        else:
            ucb = Vi + 2.0 * np.sqrt(np.log(N) / n)
        return ucb

    def isHighestUCBNode(self):
        curUCB = self.getSingleUCB()
        siblingsList = list(self.siblings)
        ucbList = [node.getSingleUCB() for node in siblingsList]
        if curUCB > max(ucbList):
            return True
        else:
            return False


    def selectUCBFromChildren(self):
        ## For the currentParentNode,
        ##get the childNodes, and selectBestUCB from them
        ##walk into it??? or just return the best one???
        ##maybe just return best one, for now...?

        ucbList = []
        childList = []
        childList = self.getDirectChildNodes()
        if self.getDirectChildNodes() == None:
            return None

        for x in range(len(childList)):
            temp = childList[x]
            n = temp.getVisited()
            Vi = temp.getValue()
            N = temp.parent.getVisited()
            if n==0:
                ucb = math.inf
            else:
                ucb = Vi + 2.0* np.sqrt( np.log( N ) / n  )
            ucbList.append(ucb)

        if len(childList) > 0:
            maxind = ucbList.index( max(ucbList)  )
            bestUCB = childList[maxind]
            return bestUCB
        else:
            return None ##This signifies that the current calling node, must have been itself
                        ##theLeafNode, and we have to use that informatoin in the mctsClass iterator to include it, but stop afterwards
                        ##EDITED::! this was impossible to do at the API so it was just stopped at leafNode with stopfilterfunc






