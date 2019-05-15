import numpy as np
from anytree import NodeMixin, RenderTree
from anytree import Node, AsciiStyle, PreOrderIter, LevelOrderIter
from treeboard import Tree_Board_State
from anytree import Walker
import copy


"""selectorFunc for the tree-iterator PreOrderIter for mcts"""
def filterUCB(parentNode):
    temp = parentNode.selectUCBFromChildren()
    return temp

def filterUCB1(node):
    """we must compare each Node with ucb computation somehow, how to do it???
    -use preOrderIter strategy, use the stopfilter1() stopfunc
    -trueRootNode is passed thru filterUCB1, return true
    -for other nodes, get siblingsNodes as a list, computeUCB for all listElements, and if
    the node that was passed as parameter, is the highestUCBnode, then return true, else return false
    """
    if node.is_root == True:
        return True
    else:
        res = node.isHighestUCBNode()
        return res



"""old stopFilterFunc for the tree-iterator PreOrderIter for mcts"""
def stopfilter1(node):
    ##stop at leaf node???
    temp = node.selectUCBFromChildren()
    if temp == None:
        return True
    else:
        return False

"""should be the currently used stopFilterFunc for the tree-iterator PreOrderIter for mcts"""
def stopfilter2(node):
    res = node.isLeafNode()
    return res





class MCTSalgo:
    """MCTS object
    -performs mcts algo on high level
    -required datamembers are as follows
        *walker obj to traverse gametree

        *rootNode to know the root, and switch root, when getting
        humanplayer's inputs into the system, and when changing the currentGameState

        *traversed path until including leafnode / or terminalnode, list of nodes
        is required for walker object to traverse one-depth at a time, into the leaf,
        and with traversedPath we can go straight back in rolloutMode, and update values,
        and visitedcounts

        *must be able to interact with getting inputs from the player,
        and gives outputs to the player after having played AI turn
        interaction can probably be tweaked at the last stage, because debugging and
        getting the mcts to work is the hard part"""

    """constructor"""
    def __init__(self ):
        self.rootNode = Tree_Board_State( np.zeros((3,3)),0,0,0,   "theRootNode", 0,0, parent=None, children=None )
        self.theWalker = Walker()
        self.traversedPath = [self.rootNode]

    """changeRootNode
    purpose is to change into new rootNode when curGameState changes (after AI has moved, or humanplayer has moved)"""
    def changeRootNode(self, newRootNode):
        self.rootNode = newRootNode
        self.rootNode.parent = None


    def getPlayerInput(self, curTreeBoard):
        self.changeRootNode( curTreeBoard )
        self.clearTraversed() ##IMPORTANT to clear the oldTraversed path because theOldTraversed points to a tree, whose root was different!
    """we can also say that the AI always takes second turn...
    hence we should always have possible gameState in the childNode, to place the marker into...
    hence, we can expand the rootNode into childNodes always"""
  #      listB, expandRes = self.rootNode.getPossibleActions()
   #     self.rootNode.expandCurrentNode(listB)


    """walkUntilLeaf (including LeafNode)
    traverses the tree from curRoot, until including leafNode, 
    meanwhile selecting the best childNodes along the path with UCB metrics
    saves the traversedPath list into memory for backpropagation purposes, 
    and also returns the leafNode itself"""

    def walkUntilLeaf(self):
        #curNode = self.rootNode
        self.traversedPath = [ node for node in PreOrderIter(self.rootNode, filter_=filterUCB1, stop=stopfilter2 ) ]
        lastNode = self.traversedPath[-1]
        self.traversedPath.append( lastNode.selectUCBFromChildren() )
        """##sadly the API was badly done, and it wasnt possible to
        ## easily walk until (including) the leafNode with stopfunction filter
        ## so we must have that "realLeafNode" append, in the end"""
        trueLeafNode = self.traversedPath[-1] #append it!
        return trueLeafNode

    def walkerFuncTraversal(self):
        destNode = self.rootNode.selectUCBFromChildren()
        if destNode == None:
            return self.rootNode
        else:
            curNode = self.rootNode
            while destNode != None:
                res = self.theWalker.walk( curNode, destNode  )
                res = res[2][0]
                self.traversedPath.append( res )
                curNode = destNode
                destNode = curNode.selectUCBFromChildren()
                ##if curNode selectUCBChildren returns None, it will have been
                ## leafNode itself
            return curNode


    def backpropagate(self, curReward):
        for x in self.traversedPath:
            x.visited_count += 1
            x.value += curReward
        kakka = 77 #for debug only



    """MAIN MCTS ALGORITHM"""
    def performMonteCarloTreeSearch(self, iterationsAmount):
        for j in range(1,iterationsAmount+1):
            leafNode = self.walkerFuncTraversal()
            if leafNode.getVisited() == 0:
                ##make Rolloout
                reward = self.playRollout(leafNode)
                self.backpropagate(reward)
            else:
                ##select childNode from expandedOnes
                ##make Rollout
                actionsList, res = leafNode.getPossibleActions()
                if  res == False: ##NotTerminalNode where game ends
                    leafNode.expandCurrentNode(actionsList)
                    childNode = leafNode.selectUCBFromChildren() ##select childNode
                    self.traversedPath.append(childNode)
                    reward = self.playRollout(childNode)
                    self.backpropagate(reward)
                else:   ##Game must have ended in this branch
                    kakka = 10 #for debug only!
                    reward = self.playRollout(leafNode)
                    self.backpropagate(reward)
            self.clearTraversed()
        print("gameTree after AI_mcts_deliberations:\n", RenderTree(self.rootNode).by_attr())

        childList = list(self.rootNode.children)
        visitsList=[]
        for child in childList:
            visitsList.append(child.getVisited())
        """mostVisited =  childList[visitsList.index(max(visitsList))  ]"""
        highVisitCount = max(visitsList)
        for child in childList:
            if child.getVisited() == highVisitCount:
                bestOpt = child
        bestOpt = copy.deepcopy(bestOpt)
        bestOpt.parent=None
        if bestOpt.current_turn == 1:
            bestOpt.current_turn = 0
        else:
            bestOpt.current_turn = 1
        return bestOpt




    """playRollout
    function is doing the mcts rollouts
    the key trick is to make the rollouts in a separateSimulatedCopy tree
    so it doesn't disturb the real mcts object's tree, then we simply 
    start from the copied gamestate simulatedRootNode, and expand the gameTree until game ends and we get
    reward.
    Other things to note about it: 
        *it will simply expand the simulatedRootNode into a gametree (until game ends) and hopefully
        garbagecollector will do something about it later...
        
        *actionPolicy for both players in rollout simulation will be equiprobable random, from the available
        actions that are left on the board"""
    def playRollout(self, originNode):
        #protip, use deepcopy instead of python shenanigans!!!
        simulatedRootNode = copy.deepcopy(originNode) ##hopefully copies the originNode into separate SimulatedRootNOde
        simulatedRootNode.parent = None
        curState = copy.deepcopy(simulatedRootNode)
        curReward = 0
        while True:
            game_res = curState.checkGameResult()
            if game_res != 2:
                if game_res == 1:
                    curReward = 50##AI has won, markers are 1s
                    break
                elif game_res == -1:
                    curReward = -50 ##human has won
                    break
                else:
                    curReward=25 ##draw
                    break
            else:
                action = curState.getRandomAction()
                if action != None:
                    curState = curState.makeLegalMove(action)
                else:
                    kakka = 90 #for debug only!

        return curReward


    def clearTraversed(self):
        self.traversedPath = [self.rootNode]

    def checkIfNoVisits(self, theNode):
        return theNode.getVisited()

