from square import *
from goal import *
from gui import *
from history import *
from prediction import * 
from collections import deque


class Moving():
    def __init__(self,grid,squares,goals):
        self.grid = grid
        self.squares = squares
        self.goals = goals
        self.gameOver = False
        self.win = False
        self.history = History()
    
    def cannotMove(self, square, dx, dy):
        nextRow, nextCol = square.row + dx, square.column + dy
        for otherSquare in self.squares:
            if (otherSquare.row == nextRow and otherSquare.column == nextCol
                    and otherSquare.color != square.color):
                return True
        return False
    
    
    def canMove(self,x,y,direction):
        if (x<0 or x >= self.grid.shape[0] or 
            y<0 or y >= self.grid.shape[1]):
            return False
        
        if self.grid[x][y] == 'F':
            self.gameOver = True
            return False
        
        if self.grid[x][y] == 'B':
            return False
        
        if self.grid[x][y] == 'W':
            return True 
        
        return False
    
    
    def sortedSquares(self,direction):
        sortedSquares = self.squares.copy()
        if  direction == 'right':
            sortedSquares.sort(key=lambda s: -s.column)
            return sortedSquares
        
        elif direction == 'left':
            sortedSquares.sort(key=lambda s: s.column)
            return sortedSquares
        
        elif direction == 'up':
            sortedSquares.sort(key=lambda s: s.row)
            return sortedSquares
        
        elif direction == 'down':
            sortedSquares.sort(key=lambda s: -s.row)
            return sortedSquares
        
        else:
            return sortedSquares
    
    
    def coloringGrayGoals(self,grayGoals):
        for graygoal in grayGoals:
                    for goal in self.goals:
                        if(graygoal['row'] == goal.row and graygoal['column'] == goal.column and goal.color == 'gray'):
                            goal.color = graygoal['newColor']
    
    def move(self,direction):
        direstionsMap = {
            'right' : (0,1),
            'left' : (0,-1),
            'up' : (-1,0),
            'down' : (1,0)
        }
        occupiedPositions = set()
        grayGoals = []
        newSquares = []
        goalsToRemove = []
        
        dx,dy = direstionsMap[direction]
        sortedSquares = self.squares.copy()
        sortedSquares = self.sortedSquares(direction)
        for square in sortedSquares:
            newX ,newY = square.row , square.column
            lastValidX , lastValidY = newX , newY
            reachedGoal = False
            reachedGoalObject = None 
            
            while (self.canMove(newX+dx,newY+dy,direction) and not self.cannotMove(square, dx, dy)):
                lastValidX , lastValidY = newX , newY
                newX += dx
                newY += dy
                
                if (newX,newY) in occupiedPositions:
                    newX , newY= lastValidX,lastValidY
                    break
                
                for goal in self.goals:
                    if(newX == goal.row and newY == goal.column and goal.color == 'gray'):
                        grayGoals.append({'row':goal.row , 'column':goal.column , 'newColor':square.color})
                    
                    if(newX == goal.row and newY == goal.column and square.color == goal.color):
                        reachedGoal = True
                        reachedGoalObject = goal
                        break
                
                if reachedGoal:
                    break
                
            if reachedGoal:
                goalsToRemove.append(reachedGoalObject)
            
            else:
                newSquare = Square(newX,newY,square.color)
                newSquares.append(newSquare)
                occupiedPositions.add((newX,newY))
                
            self.coloringGrayGoals(grayGoals)
            
        for goal in goalsToRemove:
            if goal in self.goals:
                self.goals.remove(goal)
                
        self.squares = newSquares
        self.history.addToHistory(direction ,self.squares, self.goals)
        return self.squares,goalsToRemove
    
    
    def isGameEnd(self):
        if self.gameOver:
            return 'gameOver'
        if len(self.goals) == 0:
            return 'win'
