import random #used for random start configuration
import time
''' Conway's Game of Life
        Rules:
            1) Live cell with fewer than 2 live neighbors dies
            2) Live cell with 2 or 3 neighbors lives to next generation
            3) Live cell with greater than 3 neighbors dies
            4) Dead cell with 3 live neighbors becomes live cell

    Making a board:
        makeRandomBoard(fillPercent,width,height)
        parseBoard(boardString,live,dead)
        makeBoard(liveCells,width,height)

    
'''


'''
    Makes a board of size Width x Height

    Inputs:
        fillPercent - int - amount of board to make live cells
        width - int - width of the board to make
        height - int - height of the board to make
'''
def makeRandomBoard(fillPercent=30,width=3,height=3):
    board = []
    threshold = fillPercent*0.01
    for i in range(height):
        board.append([])
        for j in range(width):
            n = random.random()
            if n < threshold:
                board[i].append(GoLCell(1))
            else:
                board[i].append(GoLCell(0))
    return board

'''
    Parses a string into a board

    input:
        boardString - str - the string version of the board
        live - str - character representing a live cell
        dead - str - character representing a dead cell

    Sample input:
        ---\n
        ###\n
        ---
'''
def parseBoard(boardString,live,dead):
    b = boardString.split('\n')
    board = []
    for i in range(len(b)):
        row = b[i]
        board.append([])
        for cell in row:
            if cell == live:
                board[i].append(GoLCell(1))
            elif cell == dead:
                board[i].append(GoLCell(0))
            elif cell == ' ':
                #ignore spaces in parsing
                #don't raise the error message
                pass
            else:
                print "Couldn't parse \"" + cell + '"'
    return board

'''
    Make a board with the list of tuples of live cell coordinates
'''
def makeBoard(liveCells,width,height):
    board = []
    for i in range(height):
        board.append([])
        for j in range(width):
##            print '('+str(i)+','+str(j)+')'
            if (i,j) in liveCells:
                board[i].append(GoLCell(1))
            else:
                board[i].append(GoLCell(0))
    return board

class GoLCell():
    def __init__(self,state):
        self.state = state

    def getState(self):
        return self.state

    def isDead(self):
        return not self.state

    def isAlive(self):
        return self.state

    def die(self):
        self.state = 0
        return

    def live(self):
        self.state = 1
        return

    def __str__(self):
        if self.isAlive():
            return '#'
        return '-'

    def __repr__(self):
        return self.__str__()
        

class GoLBoard():
    def __init__(self,board):
        self.generation = 0
        self.board = board

    def update(self):
        temp_board = []
        for i in range(len(self.board)):
            temp_board.append([])
            row = self.board[i]
            for j in range(len(row)):
                cell = self.board[i][j]
                temp_board[i].append(GoLCell(cell.getState()))
                temp_cell = temp_board[i][j]
                neighborsSum = self.getNeighborsSum(i,j)
##                print '('+str(i)+','+str(j)+')'
                if cell.isAlive():
                    if (neighborsSum != 2) and (neighborsSum != 3):
                        temp_cell.die()
                elif cell.isDead():
                    if (neighborsSum == 3):
                        temp_cell.live()
                else:
                    print 'Error updating cell (' + str(i) + ',' + str(j) + ')'
        self.board = temp_board
        self.generation += 1
        return

    def getNeighborsSum(self,x,y):
##        print 'Neighbors of: ('+str(x)+','+str(y)+')'
        total = 0
        deltas = [-1,0,1]
        for i in deltas:
            for j in deltas:
                newCellX = x + i
                newCellY = y + j
                if not ((newCellX == x) and (newCellY == y)): #if we're not in our cell
                    if (newCellX >= 0) and (newCellY >= 0):
                        try:
                            total += self.board[newCellX][newCellY].getState()
                        except: #if the board doesn't have that cell
                            total += 0
        return total

    def getGeneration(self):
        return self.generation

    def isBoardDead(self):
        '''
            Returns true if there are no more live cells on the board
        '''
        for row in self.board:
            for cell in row:
                if cell.isAlive(): # if even one cell is alive, return false
                    return False
        return True

    def __str__(self):
        rep = 'Generation '+str(self.generation)+': \n'
        for row in self.board:
            for column in row:
                rep += str(column)
                rep += ' '
            rep += '\n'
        return rep

    def __repr__(self):
        rep = ''
        for row in self.board:
            for column in row:
                rep += str(column)
                rep += ' '
            rep += '\n'
        return rep

def wait():
    raw_input("")
##    time.sleep(5)
    
def main():
    MAX_GENERATIONS = 1000 #maximum generations to calculate
    # Make random board
    a = makeRandomBoard(width=10,height=10)
    # Make a board from a set of live cells
##    width = 37
##    height = 9
##    liveCells = [(0,0),(0,1),(1,0),(1,1),(2,6),(2,18),(2,19),(2,20),(2,21),
##                 (3,6),(4,6),(5,15),(5,16),(5,25),(6,15),(6,17),(6,25),
##                 (6,26),(7,15),(7,25),(7,26),(7,35),(7,36),(8,26),(8,35),
##                 (8,36)]
##    a = makeBoard(liveCells,width,height)
    # Make a board from a string
##    a = parseBoard(cool_start,'#','-')
    g = GoLBoard(a)
    print g
    wait()
##    while g.getGeneration() < MAX_GENERATIONS: #run for MAX_GENERATIONS
    while True: #run indefinitely
        g.update()
        print g
        wait()
    return

cool_start = '''
- - - - - # # # # # 
- - - - - - - # - # 
- - # - # - - - - - 
- - # # # - # - - - 
- # - - # # - # # - 
- - # - - - # - # # 
# # - - - - - - # # 
- # - - - - # - # # 
- # # - # - # # - - 
- - - - - # - - - -
'''
