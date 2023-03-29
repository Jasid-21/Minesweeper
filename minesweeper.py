import numpy as np
import random

abc = "abcdefghijklmnopqrstuvwxyz"
size = 15
array = []
matrix = []

def reveal_safe_cells(matrix, row, col):
    cell = matrix[row][col]
    if cell.check_for_mine() or cell.reveled:
        return
    cell.reveal()
    if cell.mines == 0:
        for r in range(max(0, row - 1), min(len(matrix), row + 2)):
            for c in range(max(0, col - 1), min(len(matrix[0]), col + 2)):
                reveal_safe_cells(matrix, r, c)


def print_matrix (matrix):
    print (" ", end= " ")
    for i in np.arange(size):
        print (abc[i] , end= " ")
    print ("")
    for i, row in enumerate(matrix):
        print (abc[i], end= " ")
        for box in row:
            print (box.get_value(), end= " ")
        print("")

def setOrNot (percent = 10):
    value = int(random.random()*100)

    if (value < percent):
        return True
    return False

class Board:
    def __init__(self, score = 0, over = False):
        self.score = score
        self.over = over
    
    def game_over (self):
        self.over = True
    
    def gain_score (self):
        self.score += 1

    pass

class Box:
    def __init__(self, mines = 0, isMine = False, marked = False, reveled = False):
        self.mines = mines
        self.isMine = isMine
        self.marked = marked
        self.reveled = reveled
    
    def check_for_mine (self):
        return self.isMine
    
    def setAsMine (self):
        self.isMine = True
    
    def markUnmark (self):
        self.marked = not self.marked
    
    def get_value (self):
        if self.reveled and not self.isMine:
            if (self.mines > 0):
                return str(self.mines)
            return "_"
        if self.isMine and self.reveled:
            return "x"
        if self.marked:
            return "o"
        return "."
    
    def add_mine (self):
        self.mines += 1
    
    def remove_mine (self):
        self.mines -= 1
    
    def reveal (self):
        self.reveled = True
    pass




# Main code...
# Create base matrix
board = Board()

for i in np.arange(size):
    temp = []
    for j in np.arange(size):
        box = Box()
        temp.append(box)
    matrix.append(temp)


# Set values
for i, row in enumerate(matrix):
    for j, box in enumerate(row):
        perc = setOrNot()
        if (perc):
            box.setAsMine()

            for ni in np.arange(i - 1, i + 2):
                for nj in np.arange(j - 1, j + 2):
                    if ni > 0 and ni < size and nj > 0 and nj < size:
                        matrix[ni][nj].add_mine()
                    if ni == i and nj == j:
                        matrix[i][j].remove_mine()


print ("In order to interact with the game use commands. For example:")
print ("<ag> without <> to reveal the ag coordinate.")
print ("<ag, m> without <> to mark ag coordinate as unsafe.")
print("")
print("")

print_matrix(matrix)

def check_command(cm):
    if cm == "":
        print ("Please enter a valid command...")
        return
    
    ar = cm.split(", ")
    coord = ar[0]
    act = ""

    if len(ar) > 1:
        act = ar[1]

        if act != "m" and act != "M":
            print ("Please enter a valid action. m or M: mark or unmark as unsafe.")
            return
    
    if len(coord) > 2:
        print ("Please, enter a valid coordinate...")
        return
    
    i = abc.find(coord[0])
    j = abc.find(coord[1])

    if i < 0 or i > size or j < 0 or j > size:
        print ("Please, enter a valid coordinate...")
        return
    
    if act != "":
        matrix[i][j].markUnmark()
        return
    
    isMine = matrix[i][j].check_for_mine()
    if isMine:
        board.game_over()
        return
    
    reveal_safe_cells(matrix, i, j)
    board.gain_score()



while not board.over:
    cm = input("Command:  ")

    check_command(cm)

    if board.over is False:
        print_matrix (matrix)

for row in matrix:
    for box in row:
        if box.check_for_mine():
            box.reveal()

print("")
print_matrix(matrix)
print ("Score: " + str(board.score))
