import numpy as np
import numpy.linalg as LA
import random
from datetime import datetime
from numpy import random as npRAND
import time
from anytree import Node, RenderTree, NodeMixin, AsciiStyle, PreOrderIter
from board import Board_State
from treeboard import Tree_Board_State
from mcts import MCTSalgo
"""    trying to implement Monte Carlo Tree Search into the tictactoe game
*most likely it wont be completely finished
*gametree will be using anytree python library (probably pip install is required for that one)
pip install anytree
*it wont be pretty looking.
*here was a good tutorial for MCTS algorithm by some indian guy online!
https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
I also took inspiration from this repo, but I could not reallly understand this dude's code really well
so it was of limited usefulness, (unlike the indian guy's tutorial, which was REALLY GOOD actually!!!)
https://github.com/int8/monte-carlo-tree-search
"""

"""    data required for MCTS algorithm:
for each state in gametree, maintain:
    *each node in gametree will be Tree_Board_State object, I think...
    *tree properties such as where is the rootNode, which are parentNode of which childNodes etc...
    *the boardState itself (it is 2D array of int, most likely I will just play tictactoe as -1, 1 instead of cross and circle, and 0 will be empty) 
    *value (t), for mcts
    *visited_count (n), for mcts
    *ucb itself can be computed at selection phase from these data, for mcts
"""

##NOTE this one was deprecated function for early testing only
def getUserInput():
    global curboard
    res = False
    while not res:
        txt = input("what is your move? (r,c) ")
        txt = txt.replace("(", "")
        txt = txt.replace(")", "")
        txt = txt.replace(",", "")
        marker = ( int(txt[0]), int(txt[1]) )
        res = curboard.isLegalMove( marker )
    return ( marker  )


#initialize basic board
# curboard = Board_State( np.zeros((3,3)), 0, 0, 0 )
# tempboard = np.zeros((3,3))
# tempboard[0,0] = 1
# keepPlaying = True


#testing anytree simple gametree
# print("\n\ntesting now basicNode with anytree and curboard\n\n")
# root_node = Node(curboard)
# #s1 = Node(, parent=root_node)
# print("gameTree was:\n", RenderTree(root_node).by_attr())


#testing NodeMixin treeboard class
# print("\n\ntesting now treeboard\n\n")
# tree_root = Tree_Board_State( np.zeros((3,3)),0,0,0,   "theRootNode", 0,0, parent=None, children=None )
# s1 = Tree_Board_State( tempboard,0,0,0, "s1Node",0,0,parent=tree_root, children=None ) ## GameTree can be increased simply by creating newNodes into somebody, who is parentNode
# print("gameTree was:\n", RenderTree(tree_root).by_attr())


# testing NodeMixin treeboard class expandingNodes for MCTS algo
# print("\n\n testing now expandingNode into possible newStatesNodes \n\n")
# actions, res = s1.getPossibleActions() ## Testing if you're able to get possible actions (row,col) tuples for newMarker into the board, based on curState, seems to work!
# s1.expandCurrentNode(actions) ## Testing if you're able to expand leafNode into all possibleNewStates, seems to work!
# print("newGameTree was:\n", RenderTree(tree_root).by_attr())
# print("rootTreeBoard was:\n", tree_root.board)
#
# testing NodeMixin treeboard get the direct childnodes, seems to work, list of nodes
# listA= s1.getDirectChildNodes() ## Testing if you're able to get childNodes as list, seems to work!
#
# testing NodeMixin treeboard selectUCB for selectionphase for MCTS algo, seems to work for initial case, returns selectedNode
# ucbNode = s1.selectUCBFromChildren() ## Testing if you're able to get node back from UCBselect, seems to return a node at least?!


# testing MCTS walkUntilLeaf, seems to work from the startingState at least
# there were lots of API usage problems in this tree-iterator, but maybe it works now
# the problem was that you couldnt easily iterate until-and-including the leafNode
#listB, expandRes = mcts.rootNode.getPossibleActions()
#mcts.rootNode.expandCurrentNode(listB)
#nodeA=mcts.walkUntilLeaf()


# testing if you can change getPlayerInput (i.e. it means to change rootNode), it seems to work nicely!
# also testing walkUntilLeaf() which seems to work nicely now
# also testing playRollout() which is the last sub-stage of the implementation of the fullMCTSAlgorithm, no results yet, still testing!... EDITED:: rollout seems to work for initialIteration rollout and backpropagations!
#leaf_node = mcts.walkUntilLeaf()
#leaf_visitcount = leaf_node.getVisited()
#if leaf_visitcount == 0:
#    mcts.playRollout(leaf_node)




"""this is the real Human Input getter func
whne you want to place your marker to the board
use format '(row,col)' indexes 0,1,2 with the comma and parenthesis included"""
def getHumanInput(realGameBoard):
    res = False
    while not res:
        print("currentBoard is as follows:\n", realGameBoard.board)
        txt = input("HUMAN, what is your move? (r,c) ")
        txt = txt.replace("(", "")
        txt = txt.replace(")", "")
        txt = txt.replace(",", "")
        markerCoords = (int(txt[0]), int(txt[1]))
        res = realGameBoard.isLegalMove(markerCoords)

    return realGameBoard.makeLegalMove(markerCoords)





"""turn0 is humanplayer turn to play
turn1 is AIplayer turn to play"""

## Initializations before game
mcts = MCTSalgo()
real_start = np.zeros((3,3))
real_root_board = Tree_Board_State( real_start, 0, 0, 0, name="realGameRootHumanStarts", length=0, width=0, parent=None, children=None )

while True:

    real_root_board = getHumanInput(real_root_board) ##getHumanInput first, human starts

    if real_root_board.checkGameResult() != 2:
        break

    mcts.getPlayerInput(real_root_board) ##pass the data to the mcts from humanInput
    ai_actions, expand_res = mcts.rootNode.getPossibleActions() ##expand the currentGameState of theAI (not sure if this was necessary, but it could be)
    mcts.rootNode.expandCurrentNode(ai_actions)
    real_root_board = mcts.performMonteCarloTreeSearch(200)
    print("AIchoicewas:\n", real_root_board.board)
    real_root_board.switchTurn()

    if real_root_board.checkGameResult()!= 2:
        break




print("\ngame ended!\n")
print("endingBoard was: \n", real_root_board.board)
print("gameTree iter at end was:\n",RenderTree(real_root_board).by_attr())


#
# print("\n\n starting the basicboard tictactoe game \n\n")
# while curboard.checkGameResult() == 2:
#     print("current_turn: player" + str(curboard.getPlayerTurn()))
#     print("board is as follows:")
#     print(curboard)
#     markerTuple = getUserInput()
#     newboard = curboard.makeLegalMove(markerTuple)
#     curboard = newboard
#
# print("game ended!")
# print("endingBoard was")
# print(curboard)




