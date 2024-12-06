from square import *
from goal import *
import heapq
from collections import deque
import sys

sys.setrecursionlimit(20000)

class Predictions:
    def __init__(self, squares, goals, grid):
        self.initialSquares = squares
        self.initialGoals = goals
        self.grid = grid
        self.graph = {}
        self.gameOver = False
        self.validState = True
        self.reQueue = []
        self.reVisited = set()
        self.reGraph = {}
        
    def cloneState(self, squares, goals):
        squares_copy = [Square(square.row, square.column, square.color) for square in squares]
        goals_copy = [Goal(goal.row, goal.column, goal.color) for goal in goals]
        return squares_copy, goals_copy
    
    def stateToKey(self, squares, goals):
        squares_key = tuple(sorted((sq.row, sq.column, sq.color) for sq in squares))
        goals_key = tuple(sorted((g.row, g.column, g.color) for g in goals))
        return (squares_key, goals_key)
    
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
        steps = 0 
        
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
                steps +=1
                
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
                
        return newSquares, goalsCopy, steps
    
    def predictMove(self, squares, goals):
        directions = ['right', 'left', 'up', 'down']
        positionsAfterMove = []
        
        for direction in directions:
            newSquares, newGoals ,steps = self.simulateMove(squares, goals, direction)
            if self.validState:
                positionsAfterMove.append({
                    'direction': direction,
                    'squares': [(sq.row, sq.column, sq.color) for sq in newSquares],
                    'goals': [(g.row, g.column, g.color) for g in newGoals],
                    'cost': steps
                })
            else:
                self.validState = True
        return positionsAfterMove
    
    
    
    def BFS(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone)
        
        queue = [(squaresClone, goalsClone, 'none', [])]
        visited = set()
        visited.add(initialStateKey)
        self.graph = {}
        
        while queue:
            currentSquares, currentGoals, lastDirection, path = queue.pop(0)
            currentStateKey = self.stateToKey(currentSquares, currentGoals)
            
            if not currentGoals:
                print('BFS')
                print('path length',len(path))
                print('path :',path)
                print('visited states :' , len(self.graph))
                #print(self.graph)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
            
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                newDirection = prediction['direction']
                newStateKey = self.stateToKey(newSquares, newGoals)
                
                if newStateKey not in visited:
                    visited.add(newStateKey)
                    self.graph[currentStateKey].append(newStateKey)
                    
                    queue.append((newSquares, newGoals, newDirection, path + [newDirection]))
        
        return None
    
    
    def DFS(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone)
        
        queue = [(squaresClone, goalsClone, 'none', [])]
        visited = set()
        visited.add(initialStateKey)
        self.graph = {}
        
        while queue:
            currentSquares, currentGoals, lastDirection, path = queue.pop()
            currentStateKey = self.stateToKey(currentSquares, currentGoals)
            
            if not currentGoals:
                print('DFS')
                print('path length',len(path))
                print('path :',path)
                print('visited states :' , len(self.graph))
                #print(self.graph)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
            
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                newDirection = prediction['direction']
                newStateKey = self.stateToKey(newSquares, newGoals)
                
                if newStateKey not in visited:
                    visited.add(newStateKey)
                    self.graph[currentStateKey].append(newStateKey)
                    
                    queue.append((newSquares, newGoals, newDirection, path + [newDirection]))
        
        return None
    
    
    def printRecursiveDFS(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        
        DFS = self.recursiveDFS(squaresClone,goalsClone,'none',[])
        #print(self.reGraph)
    
    
    def recursiveDFS(self,newSquares,newGoals,newDirection,path):
        
        self.reQueue.append((newSquares,newGoals,newDirection,path))
        stateKey = self.stateToKey(newSquares, newGoals)
        self.reVisited.add(stateKey)
        
        while self.reQueue:
            currentSquares, currentGoals, lastDirection, path = self.reQueue.pop()
            currentStateKey = self.stateToKey(currentSquares, currentGoals)
            
            if not currentGoals:
                print('Recursive DFS')
                print('path length',len(path))
                print('path :',path)
                print('visited states :' , len(self.reGraph))
                return path
            
            if currentStateKey not in self.reGraph:
                self.reGraph[currentStateKey] = []
            
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                newDirection = prediction['direction']
                newStateKey = self.stateToKey(newSquares, newGoals)
                
                if newStateKey not in self.reVisited:
                    self.reVisited.add(newStateKey)
                    self.reGraph[currentStateKey].append(newStateKey)
                    self.recursiveDFS(newSquares,newGoals,newDirection,path + [newDirection])
        
        return None
    
    
    def UCS(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone)
        priorityQueue = []
        heapq.heappush(priorityQueue, (0, initialStateKey, 'none', []))
        
        costs = {initialStateKey: 0}
        self.graph = {}
        
        while priorityQueue:
            cost, currentStateKey, lastDirection, path = heapq.heappop(priorityQueue)
            squaresKey, goalsKey = currentStateKey
            
            currentSquares = [Square(row, col, color) for row, col, color in squaresKey]
            currentGoals = [Goal(row, col, color) for row, col, color in goalsKey]
            
            if not currentGoals:
                print('UCS')
                print('path length',len(path))
                print('path :',path)
                print('visited states :' ,len(self.graph))
                print('cost :' , cost)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
            
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquaresKey = tuple(sorted((row, col, color) for row, col, color in prediction['squares']))
                newGoalsKey = tuple(sorted((row, col, color) for row, col, color in prediction['goals']))
                newDirection = prediction['direction']
                newCost = prediction['cost']
                newStateKey = (newSquaresKey, newGoalsKey)
                
                totalCost = cost + newCost
                
                if newStateKey not in costs or totalCost < costs[newStateKey]:
                    costs[newStateKey] = totalCost
                    self.graph[currentStateKey].append((newStateKey, newDirection))
                    heapq.heappush(priorityQueue, (totalCost, newStateKey, newDirection, path + [newDirection]))
        
        return None
    
    def manhattanDistance(self, square, goals):
        distances = [
            abs(square.row - goal.row) + abs(square.column - goal.column)
            for goal in goals if goal.color == square.color
        ]
        return min(distances) if distances else float('inf')
    
    def simpleHillClimbing(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        currentSquares, currentGoals = squaresClone, goalsClone
        path = []
        
        while currentGoals:
            predictions = self.predictMove(currentSquares, currentGoals)
            foundBetterMove = False
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                heuristic = sum(self.manhattanDistance(square, newGoals) for square in newSquares)
                
                if heuristic < sum(self.manhattanDistance(square, currentGoals) for square in currentSquares):
                    currentSquares = newSquares
                    currentGoals = newGoals
                    path.append(prediction['direction'])
                    foundBetterMove = True
                    break
                
            if not foundBetterMove:
                print("No better moves available. Stopping Simple Hill Climbing.")
                break
        
        print('path length',len(path))
        print('path :' , path)
        return path
    
    
    def steepestAscentHillClimbing(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        currentSquares, currentGoals = squaresClone, goalsClone
        path = []
        
        while currentGoals:
            predictions = self.predictMove(currentSquares, currentGoals)
            bestMove = None
            bestHeuristic = float('inf')
            
            for prediction in predictions:
                newSquares = [Square(row, col, color) for row, col, color in prediction['squares']]
                newGoals = [Goal(row, col, color) for row, col, color in prediction['goals']]
                heuristic = sum(self.manhattanDistance(square, newGoals) for square in newSquares)
                
                if heuristic < bestHeuristic:
                    bestHeuristic = heuristic
                    bestMove = prediction
                    
            if bestMove is None or bestHeuristic >= sum(self.manhattanDistance(square, currentGoals) for square in currentSquares):
                print("No better moves available. Stopping Steepest Ascent Hill Climbing.")
                break
            
            currentSquares = [Square(row, col, color) for row, col, color in bestMove['squares']]
            currentGoals = [Goal(row, col, color) for row, col, color in bestMove['goals']]
            path.append(bestMove['direction'])
            
        print('path length',len(path))
        print('Path :', path)
        return path
    
    def AStar(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone)
        priorityQueue = []
        heapq.heappush(priorityQueue, (0, 0, initialStateKey, 'none', []))
        
        costs = {initialStateKey: 0}
        self.graph = {}
        
        while priorityQueue:
            _, cost, currentStateKey, lastDirection, path = heapq.heappop(priorityQueue)
            squaresKey, goalsKey = currentStateKey
            
            currentSquares = [Square(row, col, color) for row, col, color in squaresKey]
            currentGoals = [Goal(row, col, color) for row, col, color in goalsKey]
            
            if not currentGoals:
                print('A*')
                print('path length',len(path))
                print('path :',path)
                print('visited states :' , len(self.graph))
                print('cost :',cost)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
                
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquaresKey = tuple(sorted((row, col, color) for row, col, color in prediction['squares']))
                newGoalsKey = tuple(sorted((row, col, color) for row, col, color in prediction['goals']))
                newDirection = prediction['direction']
                newCost = prediction['cost']
                newStateKey = (newSquaresKey, newGoalsKey)
                
                heuristic = sum(self.manhattanDistance(square, currentGoals)
                    for square in [Square(row, col, color) for row, col, color in prediction['squares']])
                totalCost = cost + newCost + heuristic
                
                if newStateKey not in costs or totalCost < costs[newStateKey]:
                    costs[newStateKey] = totalCost
                    self.graph[currentStateKey].append((newStateKey, newDirection))
                    heapq.heappush(priorityQueue, (totalCost, cost + newCost, newStateKey, newDirection, path + [newDirection]))
                    
        return None
    
    def BFSHeuristic(self,grid, start, goal):
        rows, cols = len(grid), len(grid[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = deque([(start[0], start[1], 0)])
        visited = set()
        visited.add((start[0], start[1]))
        
        while queue:
            x, y, dist = queue.popleft()
            
            if (x, y) == (goal[0], goal[1]):
                return dist
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'B' and grid[nx][ny] != 'F' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))
        
        return float('inf')


    def advancedHeuristic(self,grid, squares, goals):
        total_cost = 0
        for square in squares:
            best_path_cost = float('inf')
            for goal in goals:
                if square.color == goal.color:
                    path_cost = self.BFSHeuristic(grid, (square.row, square.column), (goal.row, goal.column))
                    best_path_cost = min(best_path_cost, path_cost)
            total_cost += best_path_cost
        return total_cost
    
    
    def advancedAStar(self):
        squaresClone, goalsClone = self.cloneState(self.initialSquares, self.initialGoals)
        initialStateKey = self.stateToKey(squaresClone, goalsClone)
        priorityQueue = []
        heapq.heappush(priorityQueue, (0, 0, initialStateKey, 'none', []))
        
        costs = {initialStateKey: 0}
        self.graph = {}
        
        while priorityQueue:
            _, cost, currentStateKey, lastDirection, path = heapq.heappop(priorityQueue)
            squaresKey, goalsKey = currentStateKey
            
            currentSquares = [Square(row, col, color) for row, col, color in squaresKey]
            currentGoals = [Goal(row, col, color) for row, col, color in goalsKey]
            
            if not currentGoals:
                print('advanced_A*')
                print('path length',len(path))
                print('path :',path)
                print('visited states :' , len(self.graph))
                print('cost :',cost)
                return path
            
            if currentStateKey not in self.graph:
                self.graph[currentStateKey] = []
                
            predictions = self.predictMove(currentSquares, currentGoals)
            
            for prediction in predictions:
                newSquaresKey = tuple(sorted((row, col, color) for row, col, color in prediction['squares']))
                newGoalsKey = tuple(sorted((row, col, color) for row, col, color in prediction['goals']))
                newDirection = prediction['direction']
                newCost = prediction['cost']
                newStateKey = (newSquaresKey, newGoalsKey)
                
                heuristic = sum(self.advancedHeuristic(self.grid, self.initialSquares, self.initialGoals)
                    for square in [Square(row, col, color) for row, col, color in prediction['squares']])
                totalCost = cost + newCost + heuristic
                
                if newStateKey not in costs or totalCost < costs[newStateKey]:
                    costs[newStateKey] = totalCost
                    self.graph[currentStateKey].append((newStateKey, newDirection))
                    heapq.heappush(priorityQueue, (totalCost, cost + newCost, newStateKey, newDirection, path + [newDirection]))
                    
        return None
