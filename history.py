from square import * 
from goal import *
import copy
from graph import *

class History:
    def __init__(self):
        self.history = []
        self.graph = Graph()
    
    
    def addToHistory(self, squares, goals):
        squareData = [(square.row, square.column, square.color) for square in copy.deepcopy(squares)]
        goalData = [(goal.row, goal.column, goal.color) for goal in copy.deepcopy(goals)]
        
        self.history.append({'squares': squareData, 'goals': goalData})
        self.printHistory()
    
    
    def printHistory(self):
        for index, state in enumerate(self.history):
            print(f'Move {index}: Squares - {state['squares']}, Goals - {state['goals']}')
    
    
    
    def getUniquePredictions(self, predictions):
        uniquePredictions = []
        
        for prediction in predictions:
            predictedSquares = sorted([(sq[0], sq[1], sq[2]) for sq in prediction['squares']])
            predictedGoals = sorted([(g[0], g[1], g[2]) for g in prediction['goals']])
            
            isUnique = True
            for state in self.history:
                historySquares = sorted(state['squares'])
                historyGoals = sorted(state['goals'])
                
                if predictedSquares == historySquares and predictedGoals == historyGoals:
                    isUnique = False
                    break
            
            if isUnique:
                uniquePredictions.append(prediction)
        
        lastEntry = self.history[-1] 
        self.graph.createNode(lastEntry, uniquePredictions)
        
        return lastEntry, uniquePredictions
