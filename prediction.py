from square import *
from goal import *

class Predictions:
    def __init__(self, squares, goals, grid):
        self.initialSquares = squares
        self.initialGoals = goals
        self.grid = grid
        self.graph = {}
        self.gameOver = False
        self.validState = True
        
    def cloneState(self, squares, goals):
        squares_copy = [Square(square.row, square.column, square.color) for square in squares]
        goals_copy = [Goal(goal.row, goal.column, goal.color) for goal in goals]
        return squares_copy, goals_copy
    
    def stateToKey(self, squares, goals, direction):
        squares_key = tuple(sorted((sq.row, sq.column, sq.color) for sq in squares))
        goals_key = tuple(sorted((g.row, g.column, g.color) for g in goals))
        return (squares_key, goals_key, direction)
    
    def cannotMove(self, square, dx, dy, squares):
        nextRow, nextCol = square.row + dx, square.column + dy
        for otherSquare in squares:
            if (otherSquare.row == nextRow and otherSquare.column == nextCol
                    and otherSquare.color != square.color):
                return True
        return False
    
    def canMove(self, x, y, direction):
        if (x < 0 or x >= self.grid.shape[0] or 
            y < 0 or y >= self.grid.shape[1]):
            return False
        if self.grid[x][y] == 'F':
            self.validState = False
            return False
        if self.grid[x][y] == 'B':
            return False
        if self.grid[x][y] == 'W':
            return True 
        return False
    
    def sortedSquares(self, squares, direction):
        sortedSquares = squares.copy()
        if direction == 'right':
            sortedSquares.sort(key=lambda s: -s.column)
        elif direction == 'left':
            sortedSquares.sort(key=lambda s: s.column)
        elif direction == 'up':
            sortedSquares.sort(key=lambda s: s.row)
        elif direction == 'down':
            sortedSquares.sort(key=lambda s: -s.row)
        return sortedSquares
    
    def coloringGrayGoals(self, grayGoals, goals):
        for graygoal in grayGoals:
            for goal in goals:
                if (graygoal['row'] == goal.row and graygoal['column'] == goal.column and goal.color == 'gray'):
                    goal.color = graygoal['newColor']
                    
    def simulateMove(self, squares, goals, direction):
        squaresCopy, goalsCopy = self.cloneState(squares, goals)
        dx, dy = {'right': (0, 1), 'left': (0, -1), 'up': (-1, 0), 'down': (1, 0)}[direction]
        
        occupiedPositions = set()
        grayGoals = []
        newSquares = []
        goalsToRemove = []
        
        sortedSquares = self.sortedSquares(squaresCopy, direction)
        
        for square in sortedSquares:
            newX, newY = square.row, square.column
            lastValidX, lastValidY = newX, newY
            reachedGoal = False
            reachedGoalObject = None
            
            while self.canMove(newX + dx, newY + dy, direction) and not self.cannotMove(square, dx, dy, squaresCopy):
                lastValidX, lastValidY = newX, newY
                newX += dx
                newY += dy
                
                if (newX, newY) in occupiedPositions:
                    newX, newY = lastValidX, lastValidY
                    break
                
                for goal in goalsCopy:
                    if newX == goal.row and newY == goal.column and goal.color == 'gray':
                        grayGoals.append({'row': goal.row, 'column': goal.column, 'newColor': square.color})
                        
                    if newX == goal.row and newY == goal.column and square.color == goal.color:
                        reachedGoal = True
                        reachedGoalObject = goal
                        break
                    
                if reachedGoal:
                    break
                
            if reachedGoal:
                goalsToRemove.append(reachedGoalObject)
            else:
                newSquare = Square(newX, newY, square.color)
                newSquares.append(newSquare)
                occupiedPositions.add((newX, newY))
                
        self.coloringGrayGoals(grayGoals, goalsCopy)
        
        for goal in goalsToRemove:
            if goal in goalsCopy:
                goalsCopy.remove(goal)
                
        return newSquares, goalsCopy
    
    def predictMove(self, squares, goals):
        directions = ['right', 'left', 'up', 'down']
        positionsAfterMove = []
        
        for direction in directions:
            newSquares, newGoals = self.simulateMove(squares, goals, direction)
            if self.validState:
                positionsAfterMove.append({
                    'direction': direction,
                    'squares': [(sq.row, sq.column, sq.color) for sq in newSquares],
                    'goals': [(g.row, g.column, g.color) for g in newGoals]
                })
            else:
                self.validState = True
        return positionsAfterMove
    
    
    
    def BFS(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone, 'none')
        
        queue = [(squaresClone, goalsClone, 'none', [])]
        visited = set()
        visited.add(initialStateKey)
        self.graph = {}
        
        while queue:
            currentSquares, currentGoals, lastDirection, path = queue.pop(0)
            currentStateKey = self.stateToKey(currentSquares, currentGoals, lastDirection)
            
            if not currentGoals:
                print(path)
                #print(self.graph)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
            
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                newDirection = prediction['direction']
                newStateKey = self.stateToKey(newSquares, newGoals, newDirection)
                
                if newStateKey not in visited:
                    visited.add(newStateKey)
                    self.graph[currentStateKey].append(newStateKey)
                    
                    queue.append((newSquares, newGoals, newDirection, path + [newDirection]))
        
        return None
    
    
    def DFS(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone, 'none')
        
        queue = [(squaresClone, goalsClone, 'none', [])]
        visited = set()
        visited.add(initialStateKey)
        self.graph = {}
        
        while queue:
            currentSquares, currentGoals, lastDirection, path = queue.pop()
            currentStateKey = self.stateToKey(currentSquares, currentGoals, lastDirection)
            
            if not currentGoals:
                print(path)
                #print(self.graph)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
            
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                newDirection = prediction['direction']
                newStateKey = self.stateToKey(newSquares, newGoals, newDirection)
                
                if newStateKey not in visited:
                    visited.add(newStateKey)
                    self.graph[currentStateKey].append(newStateKey)
                    
                    queue.append((newSquares, newGoals, newDirection, path + [newDirection]))
        
        return None
    