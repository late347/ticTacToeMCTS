import numpy as np

"""this class was just for testing basic fucntions for tictactoe
this Board_State class was just an old tester class basically

THIS CLASS IS DEPRECATED"""

class Board_State:
    x = 1
    o = -1
    #unoccupied should be zero
    #board is numpy array 3x3 of integers

    def __init__(self, the_state, whos_turn_it_is, state_value, the_visited_count):
        self.board = the_state #initialize with numpy array 3x3, filled with zeroes
        self.current_turn = whos_turn_it_is #whos turn it is
        self.value = state_value
        self.visited_count = the_visited_count


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
            return 1 #gameresult1
        elif any(rowsum == -3) or any(colsum == -3) or (diagsum1 == -3) or (diagsum2 == -3):
            return -1 #gameresult2
        elif np.all(b != 0):
            return 0 #draw was reached
        else:
            return 2 #game continues

    def isLegalMove(self ,newMarkerTuple):
        nr = newMarkerTuple[0] #row
        nc = newMarkerTuple[1] #col
        if self.board[nr, nc] == 0 and (0 <= nr <= 3 and 0 <= nc <=3): #check if newcoords is empty and newcoords are legalsize
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
            New_Board_State = Board_State(newboard, newturn, 0, 0)
            """return the newboardstate to the gaame treee, append it to it"""
            return New_Board_State

    def getPlayerTurn(self):
        return self.current_turn

    def getValue(self):
        return self.value

    def getVisited(self):
        return self.visited_count

